import re
from functools import reduce
from DBModels.Username import *
from DBModels.Tweet import *
import os
from controllers.DataCleaning import preprocessing
from controllers.DataCleaning import Patterns as pat
from controllers.Feature_Extraction import ngram_extractor
import pandas as pd
from multiprocessing import Pool
from functools import partial
import numpy as np


num_partitions = 6  # number of partitions to split dataframe
num_cores = 6  # number of cores on your machine

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "stop_words")

# loads stop words list from file
stopwords = pd.read_csv(file_path+"/final_stop_words_list.csv", header=None, squeeze=True).tolist()
# loads contractions from file
contractions = pd.read_csv(file_path+"/contractions.csv", header=None, delimiter=',')
dictionary = dict(zip(contractions[0].tolist(), contractions[1].tolist()))

c_re = re.compile('(%s)' % '|'.join(dictionary.keys()))


def read_csv(filename):
    return pd.read_csv(filename, encoding="utf8", keep_default_na=False, index_col=None,
                       sep=",", skipinitialspace=True, chunksize=10000,
                       usecols=['Id', 'Tweet', 'Username', 'Hashtags', 'Location', 'Favorites', 'Retweets',
                                'Date Created'])


def expand_contractions(text, c_re=c_re):
    def replace(match):
        return dictionary[match.group(0)]
    return c_re.sub(replace, text)


def get_usernames(tweet_list):
    pattern = re.compile("@[a-zA-Z0-9]+")
    # found_username_list = []

    return pattern.findall(tweet_list)


def anonymized_tweet(tweet, nameTuple):
    # data anonymization
    return reduce(lambda a, kv: a.replace(*kv), nameTuple, tweet)


def init_data_cleaning(tweet):
    # print ("Before:" + tweet)
    # data anonymization
    # tweet = anonymized_tweet(tweet, nameTuple)
    # removes URL, hashtags, HTML, and Reserved words
    tweet = pat.remove_from_tweet(tweet)
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

    # print("After:" + tweet)

    return tweet


def anonymize_poster_username(username_list, username_dict):
    return [username_dict['@'+u] for u in username_list]


def process_hashtags(hashtag_list):
    pattern = re.compile("^\s+|\s*,\s*|\s+$")
    return [pattern.split(hashtags) if hashtags is not '' else [] for hashtags in hashtag_list]


def parallelize_dataframe(df, func, name_tuple, usernames):
    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    func = partial(func, name_tuple, usernames)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def process_chunk(name_tuple, usernames, chunk):
    # chunk['tweet'] will hold the processed/cleaned tweet
    chunk['tweet'] = chunk.apply(lambda row: init_data_cleaning(row['Tweet']), axis=1)
    # 1-3 grams for each tweet
    chunk['unigram'], chunk['bigram'], chunk['trigram'] = ngram_extractor.get_ngrams(chunk['tweet'])
    # positive emoticon/negative emoticon count
    chunk['posemote'] = chunk.apply(lambda row: row['tweet'].count('POSEMOTE'), axis=1)
    chunk['negemote'] = chunk.apply(lambda row: row['tweet'].count('NEGEMOTE'), axis=1)
    # anonymize poster username
    chunk['Username'] = anonymize_poster_username(chunk['Username'], usernames)
    # hashtag processing
    chunk['hashtags'] = process_hashtags(chunk['Hashtags'])
    # anonymized original tweet
    chunk['Tweet'] = chunk.apply(lambda row: anonymized_tweet(row['Tweet'], name_tuple), axis=1)
    # users mentioned
    chunk['users_mentioned'] = chunk.apply(lambda row: get_usernames(row['Tweet']), axis=1)

    return chunk


def cleaning_file(file_name):
    print("Start Cleaning File")
    reader = read_csv(file_name)
    results = pd.DataFrame()

    for ctr, chunk in enumerate(reader):
        # add usernames to DB
        preprocessing.process_usernames(chunk)
        name_tuple = get_all_username_tup()
        usernames = get_all_username_dict()

        results = parallelize_dataframe(chunk, process_chunk, name_tuple, usernames)

        # this removes empty tweets after cleaning
        results.drop(results[results.tweet == ""].index, inplace=True)

        # rename some column names
        results.rename(index=str, columns={"Location": "location", "Retweets": "retweet", "Favorites": "favorite",
                                         "Date Created": "date_created", "Id": 'idTweet',
                                         "Tweet": "orig_tweets", "Username": 'idUsername'}, inplace=True)

        insert_new_tweet(results.to_dict(orient='records'))

    print("Done Cleaning File")
