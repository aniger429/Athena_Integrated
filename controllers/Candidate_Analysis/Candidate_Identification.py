from DBModels.KB_Names import *
from DBModels.Tweet import *
from controllers.Pickles.Pickle_Saver import *

import pandas as pd
from controllers.Sentiment_Analysis.Sentiment_Identification import *


def get_mention_index(tweet, candidate_names):
    # returns the position of the names used for the candidate in the tweet,
    # if candidate was not mentioned -1 is returned

    index = next((tweet.index(word) for word in tweet if any(name in word
                                                             for name in candidate_names)), -1)
    return index


def identify_candidate(tweet_df, cname="none"):
    print("cname")
    print(cname)
    # gets all the known candidate names in the database
    candidate_data = get_all_kb_names()
    candidate_names = []

    # convert all tweets to list of words
    tweet_df['orig_tweets'] = tweet_df.apply(lambda row: row['orig_tweets'].lower().split(' '), axis=1)

    # creates a new column per candidate and stores the index of word mentioned for the candidate
    for candidate in candidate_data:
        if candidate['candidate_name'] == cname:
            candidate_names = candidate['kb_names']

        tweet_df[candidate['candidate_name']] = tweet_df.apply(lambda row: get_mention_index(row['orig_tweets'],
                                                                           candidate['kb_names']), axis=1)
    # drop all the rows that did not mention cname
    if cname != "none":
        tweet_df = tweet_df[(tweet_df[cname] != -1)]

    # save tweet dataframe to pickles
    save_dataframe(tweet_df, "Candidate")

    # into_new_db(candidate_presence)
    return


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

# original_tweets()
