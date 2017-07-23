import pandas as pd
from multiprocessing import Pool
from functools import partial
import numpy as np
from controllers.Sentiment_Analysis.Sentiment_Identification import *
from DBModels.KB_Names import *


num_partitions = 6  # number of partitions to split dataframe
num_cores = 6  # number of cores on your machine
columns = ['Tweet', 'Tweet_processed', 'Binay', 'Duterte', 'Poe', 'Roxas', 'Santiago']


def read_csv(filename):
    return pd.read_csv(filename, encoding="utf8", keep_default_na=False, index_col=None,
                       sep=",", skipinitialspace=True, chunksize=100000,
                       usecols=['Tweet'])


def get_mention_index(tweet, candidate_names):
    # returns the position of the names used for the candidate in the tweet,
    # if candidate was not mentioned -1 is returned

    index = next((tweet.index(word) for word in tweet if any(name in word
                                                             for name in candidate_names)), -1)
    return index


def process_df(candidate_data, tweet_df):
    for candidate in candidate_data:
        tweet_df[candidate['candidate_name']] = tweet_df.apply(lambda row: get_mention_index(row['Tweet_processed'],
                                                               candidate['kb_names']), axis=1)
    return tweet_df


def parallelize_dataframe(df, func, candidate_data):
    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    func = partial(func, candidate_data)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def lower_split_tweet(tweet):
    return tweet.lower().split(' ')


def identify_candidate(candidate_data, tweet_df):
    # convert all tweets to list of words
    if isinstance(tweet_df['Tweet'].iloc[0], list):
        tweet_df['Tweet'] = tweet_df.apply(lambda row: row['Tweet'], axis=1)
    else:
        tweet_df['Tweet_processed'] = tweet_df.apply(lambda row: lower_split_tweet(row['Tweet']), axis=1)

    # creates a new column per candidate and stores the index of word mentioned for the candidate
    # tweet_df = parallelize_dataframe(tweet_df, process_df, candidate_data)

    tweet_df = process_df(candidate_data, tweet_df)

    return tweet_df


def parallelize_chunk(chunk, func, candidate_data):
    df_split = np.array_split(chunk, num_partitions)
    pool = Pool(num_cores)
    func = partial(func, candidate_data)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def find_more_names(tweets):
    candidate_names = get_all_kb_names()
    results = {}

    for candidate in candidate_names:
        results[candidate['candidate_name']] = list(set([word for tweet in tweets for word in tweet
                                                         if any(name in word for name in candidate['kb_names'])
                                                         and (word not in candidate['blacklist_names'])]))

    kb_names_update(results)


def write_csv(filename, tweets):
    import os
    # if file does not exist write header
    if not os.path.isfile(filename):
        return tweets.to_csv(filename, header=True, sep=',', index=False, columns=columns, chunksize=10000)
    else:  # else it exists so append without writing the header
        return tweets.to_csv(filename, mode='a', sep=',', index=False, header=False, columns=columns, chunksize=10000)


def write_data(filename, data):
    import os
    # if file does not exist write header
    if not os.path.isfile(filename):
        return data.to_csv(filename, header=True, sep=',', index=False)
    else:  # else it exists so append without writing the header
        return data.to_csv(filename, mode='a', sep=',', index=False, header=False)


def start_process(file_name):
    filepath = "/home/dudegrim/Documents/CSV8/"

    print("Start", file_name)
    reader = read_csv(filepath + file_name)
    results = pd.DataFrame()

    # gets all the known candidate names in the database
    candidate_data = get_all_kb_names()

    for ctr, chunk in enumerate(reader):
        # add usernames to DB
        results = parallelize_chunk(chunk, identify_candidate, candidate_data)

    # find_more_names(results["Tweet_processed"])

    cand_count = {}
    for candidate in candidate_data:
        cand_df = results[results[candidate['candidate_name']] >= 0]

        cand_count[candidate['candidate_name']] = len(cand_df)
        # save the stuff
        write_csv("/home/dudegrim/Documents/whole/"+candidate['candidate_name'], cand_df)

    data_count = pd.DataFrame(cand_count, index=[0])

    write_data("/home/dudegrim/Documents/whole/candidate_data_count.csv", data_count)

    return


for r in range(0, 3, 1):
    print(r)
    start_process("Election-"+str(r)+".csv")
