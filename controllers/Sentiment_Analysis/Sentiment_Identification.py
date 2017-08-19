from controllers.Pickles.Pickle_Saver import *
import pickle
import re
from multiprocessing import Pool

import numpy as np

from DBModels.Lexicon import *
from controllers.Pickles.Pickle_Saver import *

num_partitions = 6  # number of partitions to split dataframe
num_cores = 6  # number of cores on your machine


script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "Lexicon_Files")
nltk.data.path.append(script_path+"/Lexicon_Files")

afinn = Afinn(emoticons=True)
posiFile = pd.read_csv(file_path + "/positive.txt", header=None)
posi_list = posiFile[0].tolist()

nega_file = pd.read_csv(file_path + "/negative.txt", header=None)
nega_list = nega_file[0].tolist()


def lscv_sentiment(tweet_list):
    # path for classifiers
    s_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(s_path, "Pickles", "ML_Classifier")

    # load pickled classififer
    with open(os.path.join(path, 'ME.pkl'), 'rb') as fid:
        lscv_clf = pickle.load(fid)

    # predict sentiment of tweet
    return lscv_clf.predict(tweet_list)


def sa_parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def check_word(lex_list, word):
    return next((s for s in lex_list if word == s), "None")


def get_word_sentiment(tweet, posEng, negEng, posFil, negFil):
    word_list = []
    for word in tweet.split(' '):
        processed_word = re.sub('[^A-Za-z0-9@ ]+', '', word.lower())
        check_neg_eng = check_word(negEng, processed_word)
        check_neg_fil = check_word(negFil, processed_word)
        check_pos_eng = check_word(posEng, processed_word)
        check_pos_fil = check_word(posFil, processed_word)
        if check_neg_eng != "None":

            word_list.append({"word": word, "sentiment": "negative", "language": "english", "matched": check_neg_eng})
        elif check_pos_eng != "None":
            word_list.append({"word": word, "sentiment": "positive", "language": "english", "matched": check_pos_eng})
        elif check_neg_fil != "None":
            word_list.append({"word": word, "sentiment": "negative", "language": "filipino", "matched": check_neg_fil})
        elif check_pos_fil != "None":
            word_list.append({"word": word, "sentiment": "positive", "language": "filipino", "matched": check_pos_fil})
        else:
            word_list.append({"word": word, "sentiment": "neutral", "language": "", "matched": ""})
    return word_list


def compute_tweets_sentiment(tweet_list):
    posEng = get_all_words("english", "positive")
    negEng = get_all_words("english", "negative")
    posFil = get_all_words("filipino", "positive")
    negFil = get_all_words("filipino", "negative")


    # Lexicon Based
    # tweet_list = sa_parallelize_dataframe(tweet_list, lexicon_sentiment)
    # returns a list of all the words with their corresponding sentiment
    tweet_list['words_senti'] = tweet_list.apply(lambda row: get_word_sentiment(row['orig_tweets'], posEng, negEng, posFil, negFil), axis=1)
    # Machine Learning - LSVC
    tweet_list['sentiment'] = lscv_sentiment(tweet_list['tweet'])
    posi_tweets = tweet_list[tweet_list['sentiment'] == "Positive"]
    neut_tweets = tweet_list[tweet_list['sentiment'] == "Neutral"]
    neg_tweets = tweet_list[tweet_list['sentiment'] == "Negative"]

    columns = ['orig_tweets', '_id', 'tweet', 'sentiment']
    # Select the ones you want
    save_dataframe(posi_tweets.loc[:, columns], 'positive')
    save_dataframe(neut_tweets.loc[:, columns], 'neutral')
    save_dataframe(neg_tweets.loc[:, columns], 'negative')

    return posi_tweets, neut_tweets, neg_tweets


