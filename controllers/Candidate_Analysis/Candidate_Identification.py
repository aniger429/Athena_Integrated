from DBModels.KB_Names import *
from DBModels.Tweet import *
from controllers.analysis_controller.Pickle_Saver import *
import pandas as pd
from controllers.Sentiment_Analysis.Sentiment_Identification import *

def identify_candidate(tweet_list, cname="none"):
    print("cname")
    print(cname)
    # gets all the known candidate names in the database
    candidate_names = get_all_kb_names()
    # stores a dictionary, key: tweet_id, value: dictionary of tweet_cp
    candidate_presence = []

    for tweet in tweet_list:
        # key: candidate name, value: position of candidate name in a tweet, -1 for none
        tweet_cp = {}
        # for each candidate
        for candidate in candidate_names:
            tweet_cp[candidate['candidate_name']] = next((tweet['orig_tweets'].index(word)
                                                          for word in tweet['orig_tweets'] if any(name in word.lower()
                                                                                                  for name in candidate['kb_names'])), -1)
        if cname == "none":
            candidate_presence.append({'cand_ana': tweet_cp, 'tweets': tweet['orig_tweets'], '_id': tweet['_id']})
        else:
            if tweet_cp[cname] != -1:
                candidate_presence.append({'cand_ana': tweet_cp, 'tweets': tweet['orig_tweets'], '_id': tweet['_id']})


    save_obj(candidate_presence, "Candidate")
    # into_new_db(candidate_presence)

    return candidate_presence


def filter_tweet_on_candidate(cname, tweet_list):
    return [tweet for tweet in tweet_list if tweet['cand_ana'][cname] != -1]


def identify_candidate_mentioned(tweet):
    print('identify_candidate_mentioned')
    cand_presence = identify_candidate(tweet, cname="none")
    print(cand_presence)
    candidate_names = get_all_kb_names()
    mentioned_candidate1 = []

    for candidate in candidate_names:
       cname=candidate['candidate_name']

       if any(t['cand_ana'][cname] > -1 for t in cand_presence):
           mentioned_candidate1.append(cname)

    return mentioned_candidate1


def candidate_analysis_testing(num_tweets):
    # retrieve all data in the database
    tweets = get_all_tweets()
    # perform candidate analysis on all tweets
    cand = ['binay', 'duterte', 'santiago', 'roxas', 'poe']

    for c in cand:
        results = identify_candidate(tweets, c)
        # create data list to hold the processed data
        data_list = []

        [data_list.append({'Tweet': ' '.join(r['tweet']),
                           'Binay': r['cand_ana']['binay'],
                           'Duterte': r['cand_ana']['duterte'],
                           'Poe': r['cand_ana']['poe'],
                           'Roxas': r['cand_ana']['roxas'],
                           'Santiago': r['cand_ana']['santiago']}) for r in results]
        # create a dataframe
        data = pd.DataFrame(data_list, columns=['Tweet','Binay', 'Duterte', 'Poe', 'Roxas', 'Santiago'])
        print("saving")
        # save to excel
        data.to_csv("/home/dudegrim/Documents/Testing/"+c+"_candidate_analysis_output.csv", sep=',',
                    columns= ['Tweet','Binay', 'Duterte', 'Poe', 'Roxas', 'Santiago'], index=None)


# candidate_analysis_testing(5000)
def test_identify_candidate(df, cname="none"):
    # gets all the known candidate names in the database
    candidate_names = get_all_kb_names()
    # stores a dictionary, key: tweet_id, value: dictionary of tweet_cp
    candidate_presence = []

    for tweet in df:
        # key: candidate name, value: position of candidate name in a tweet, -1 for none
        tweet_cp = {}
        # for each candidate
        for candidate in candidate_names:
            tweet_cp[candidate['candidate_name']] = next((1 for word in tweet['orig_tweets'] if any(name in word.lower()
                                                                                                    for name in candidate['kb_names'])), 0)

        # tweet_cp.update({'orig_tweets': tweet})
        if not all(value == 0 for value in tweet_cp.values()):
            tweet['orig_tweets'] = ' '.join(tweet['orig_tweets'])
            tweet.update(tweet_cp)
            candidate_presence.append(tweet)

    return candidate_presence

import pandas
import time

def write_csv(df):
    df.to_csv("/home/dudegrim/Documents/Testing/guada_tweets2.csv", sep=',',
                columns=['orig_tweets', 'tweet', 'binay', 'duterte', 'poe', 'roxas', 'santiago', 'sentiment'], index=None)

    return


def read_csv(filename):
    data = pandas.read_csv(filename, sep=',', index_col=None)
    return data

from multiprocessing import Pool
import numpy as np

num_partitions = 6  # number of partitions to split dataframe
num_cores = 6  # number of cores on your machine


def parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def multiply_columns(tweets):
    print("done 1")
    tweets['sentiment'] = tweets.apply(lambda row: test_senti_ana(row['tweet']), axis=1)
    return tweets


def senti():

    tweets = read_csv("/home/dudegrim/Documents/Testing/guada_tweets1.csv")

    print("start")
    start = time.time()
    results = parallelize_dataframe(tweets, multiply_columns)
    end = time.time()

    print(end - start)
    print("sentiment analysis done")

    write_csv(tweets)


def candi():
    tweets = get_all_orig_tweets()

    results = test_identify_candidate(tweets)
    print("candidate analysis done")

    df1 = pandas.DataFrame(results)

    print(len(df1.index))

    write_csv(df1)


def check_data():
    df = read_csv("/home/dudegrim/Documents/Testing/guada_tweets1.csv")
    # final = df[(df['duterte'] == 1)].head(n=10000)
    # final.append(df[(df['roxas'] == 1)].head(n=10000), ignore_index=False)
    # final.append(df[(df['binay'] == 1)].head(n=10000), ignore_index=False)
    # final.append(df[(df['santiago'] == 1)].head(n=10000), ignore_index=False)
    # final.append(df[(df['poe'] == 1)].head(n=10000), ignore_index=False)

    final = df.drop(df[(df.duterte == 1) & (df.binay == 0) & (df.santiago == 0) & (df.roxas == 0) & (df.poe == 0)].index)

    print(len(final[(final['binay'] == 1)]))
    print(len(final[(final['duterte'] == 1)]))
    print(len(final[(final['santiago'] == 1)]))
    print(len(final[(final['roxas'] == 1)]))
    print(len(final[(final['poe'] == 1)]))

    write_csv(final)
check_data()
