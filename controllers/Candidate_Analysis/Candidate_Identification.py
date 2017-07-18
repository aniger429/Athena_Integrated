from DBModels.KB_Names import *
from DBModels.Tweet import *
import pandas as pd
from controllers.Sentiment_Analysis.Sentiment_Identification import *
from multiprocessing import Pool
from functools import partial
import numpy as np


num_partitions = 6  # number of partitions to split dataframe
num_cores = 6  # number of cores on your machine


def get_mention_index(tweet, candidate_names):
    # returns the position of the names used for the candidate in the tweet,
    # if candidate was not mentioned -1 is returned

    index = next((tweet.index(word) for word in tweet if any(name in word
                                                             for name in candidate_names)), -1)
    return index


def process_df(candidate_data, tweet_df):
    for candidate in candidate_data:
        tweet_df[candidate['candidate_name']] = tweet_df.apply(lambda row: get_mention_index(row['orig_tweets'],
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


def identify_candidate(tweet_df, cname="none"):
    # gets all the known candidate names in the database
    candidate_data = get_all_kb_names()

    # convert all tweets to list of words
    if isinstance(tweet_df['orig_tweets'].iloc[0], list):
        tweet_df['orig_tweets'] = tweet_df.apply(lambda row: row['orig_tweets'], axis=1)
    else:
        tweet_df['orig_tweets'] = tweet_df.apply(lambda row: lower_split_tweet(row['orig_tweets']), axis=1)

    # creates a new column per candidate and stores the index of word mentioned for the candidate
    tweet_df = parallelize_dataframe(tweet_df, process_df, candidate_data)

    # drop all the rows that did not mention cname
    if cname != "none":
        tweet_df = tweet_df[(tweet_df[cname] != -1)]

    # save tweet dataframe to pickles
    save_dataframe(tweet_df, "Candidate")

    # into_new_db(candidate_presence)
    return tweet_df


def filter_tweet_on_candidate(cname, tweet_list):
    return [tweet for tweet in tweet_list if tweet['cand_ana'][cname] != -1]


def identify_candidate_mentioned(tweet):
    candidate_names = get_all_kb_names()
    if not any(candidate['candidate_name'] in tweet.columns for candidate in candidate_names):
        tweet = identify_candidate(tweet)

    return [candidate['candidate_name'] for candidate in candidate_names
            if (len(tweet[(tweet[candidate['candidate_name']] != -1)]) > 0)]


def candidate_analysis_testing(num_tweets):
    # retrieve all data in the database
    tweets = get_all_orig_tweets()[:num_tweets]
    # perform candidate analysis on all tweets
    cand = ['binay', 'duterte', 'santiago', 'roxas', 'poe']

    for c in cand:
        results = identify_candidate(tweets, c)
        # create data list to hold the processed data
        print(results)
        data_list = []

        [data_list.append({'Tweet': ' '.join(r['tweets']),
                           'Binay': r['cand_ana']['binay'],
                           'Duterte': r['cand_ana']['duterte'],
                           'Poe': r['cand_ana']['poe'],
                           'Roxas': r['cand_ana']['roxas'],
                           'Santiago': r['cand_ana']['santiago']}) for r in results]
        # create a dataframe
        data = pd.DataFrame(data_list, columns=['Tweet', 'Binay', 'Duterte', 'Poe', 'Roxas', 'Santiago'])
        print("saving")
        # save to excel
        data.to_csv("/home/dudegrim/Documents/Testing/"+c+"_candidate_analysis_output.csv", sep=',',
                    columns=['Tweet', 'Binay', 'Duterte', 'Poe', 'Roxas', 'Santiago'], index=None)


def original_tweets():
    tweets = get_all_orig_tweets()
    df = pd.DataFrame(tweets)
    df['orig_tweets'] = df.apply(lambda row: ' '.join(row['orig_tweets']), axis=1)
    df.to_csv("/home/dudegrim/Documents/Testing/original_tweets.csv", sep=',',
                columns=['orig_tweets', 'tweet'], index=None)


def candidate_analysis(tweets, candidate_name):
    #  do candidate analysis on the tweets
    identify_candidate(tweets, candidate_name)

    # load data from pickles
    data = load_pickled_dataframe("Candidate")
    # get all the names used to mention the candidate
    data['name'] = data.apply(lambda row: (row['orig_tweets'][row[candidate_name]]), axis=1)
    # get a frequency count
    candidate_name_count = Counter(list(data['name']))

    return candidate_name_count, data
