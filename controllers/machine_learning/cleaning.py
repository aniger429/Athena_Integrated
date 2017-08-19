import os
import re
from multiprocessing import Pool

import numpy as np
import pandas as pd

from controllers.DataCleaning import Patterns as pat
from controllers.DataCleaning import emojip as ep

num_partitions = 6  # number of partitions to split dataframe
num_cores = 6  # number of cores on your machine

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "stop_words")

# loads stop words list from file
stopwords = pd.read_csv(file_path + "/final_stop_words_list.csv", header=None, squeeze=True).tolist()
# loads contractions from file
contractions = pd.read_csv(file_path + "/contractions.csv", header=None, delimiter=',')
dictionary = dict(zip(contractions[0].tolist(), contractions[1].tolist()))

c_re = re.compile('(%s)' % '|'.join(dictionary.keys()))

removeSp = re.compile(r'@(\w+)')
posi_list = ep.pos_file_to_list()  # get positive list from positive.txt
nega_list = ep.neg_file_to_list()  # get negative list from negative.txt


def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8', keep_default_na=False)


def expand_contractions(text, c_re=c_re):
    def replace(match):
        return dictionary[match.group(0)]

    return c_re.sub(replace, text)


def emoji_processing(tweet):
    tweet = ep.pos(tweet, posi_list)  # replace all positive emojis (written in positive.txt) to 'POSITIVEEMOTICON'
    tweet = ep.neg(tweet, nega_list)  # replace all negative emojis (written in positive.txt) to 'NEGATIVEEMOTICON'
    tweet = data_cleaning(tweet)  # data cleaning and so on.
    tweet = removeSp.sub('', tweet)

    return tweet


# Data Cleaning used by Sentiment Analysis (Machine Learning)
def data_cleaning(tweet):
    # removes Username, URL, Reserved Words
    tweet = pat.remove_from_tweet_sentiment(tweet)
    # converts the tweets to lowercase
    tweet = tweet.lower()
    # expand contradictions
    tweet = expand_contractions(tweet)

    split_tweet = tweet.split(' ')
    split_tweet = filter(None, split_tweet)

    # standardize words collapse to 2 letter ex: cooool to cool
    tweet = ' '.join([(re.sub(r'(.)\1+', r'\1\1', word)) if word[0] != '@' else word for word in split_tweet])

    # processes emoticons
    # positive
    tweet = re.sub("[:;8=x][-oc]*[>D)}P\]3]+", "POSEMOTE", tweet)
    tweet = re.sub("[<({\[]+[-o]*[:;8=x]", "POSEMOTE", tweet)

    tweet = re.sub("[:;8=x][-oc]*[<({\[]+", "NEGEMOTE", tweet)
    tweet = re.sub("[>D)}\]]+[-o]*[:;8=x]", "NEGEMOTE", tweet)

    # remove punctuation marks
    tweet = re.sub('[^A-Za-z0-9@ ]+', ' ', tweet)

    split_tweet = tweet.split(' ')

    # remove stopwords
    split_tweet = [word for word in split_tweet if word not in stopwords]

    # remove shortwords 1-2 characters
    split_tweet = [word for word in split_tweet if len(word) > 1]

    # remove extra spaces between words
    tweet = ' '.join(split_tweet)
    return tweet


def clean(chunk):
    chunk['Tweet'] = chunk['Tweet'].apply(lambda x: data_cleaning(x))
    return chunk


def parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def clean_tweets_multiprocess(chunk):
    results = parallelize_dataframe(chunk, clean)
    return results
