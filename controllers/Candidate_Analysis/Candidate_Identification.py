from DBModels.KB_Names import *
from DBModels.Tweet import *
from controllers.analysis_controller.Pickle_Saver import *
import pandas as pd

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
            tweet_cp[candidate['candidate_name']] = next((tweet['tweet'].index(word) for word in tweet['tweet'] if any(name in word for name in candidate['kb_names'])), -1)

        if cname == "none":
            candidate_presence.append({'cand_ana': tweet_cp, 'tweet': tweet['tweet'], '_id': tweet['_id']})
        else:
            if tweet_cp[cname] != -1:
                candidate_presence.append({'cand_ana': tweet_cp,'tweet':tweet['tweet'], '_id': tweet['_id']})


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

    results = identify_candidate(tweets, "none")
    # create data list to hold the processed data
    data_list = []

    [data_list.append({'Tweet': ' '.join(r['tweet']),
                       'Binay': r['cand_ana']['binay'],
                       'Duterte': r['cand_ana']['duterte'],
                       'Poe': r['cand_ana']['poe'],
                       'Roxas': r['cand_ana']['roxas'],
                       'Santiago': r['cand_ana']['santiago']}) for r in results[:num_tweets]]
    # create a dataframe
    data = pd.DataFrame(data_list, columns=['Tweet','Binay', 'Duterte', 'Poe', 'Roxas', 'Santiago'])
    print("saving")
    # save to excel
    data.to_csv("/home/dudegrim/Documents/Testing/candidate_analysis_output.csv", sep=',',
                columns= ['Tweet','Binay', 'Duterte', 'Poe', 'Roxas', 'Santiago'], index=None)


# candidate_analysis_testing(5000)
