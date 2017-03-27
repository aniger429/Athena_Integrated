from DBModels.KB_Names import *
from DBModels.Tweet import *
from controllers.analysis_controller.Pickle_Saver import *


def identify_candidate(tweet_list, cname):
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

              # tweet_cp[candidate['candidate_name']] = ([tweet['tweet'].index(word) for word in tweet['tweet'] if any(name in word for name in candidate['kb_names'])])
        if tweet_cp[cname] != -1:
            candidate_presence.append({'cand_ana':tweet_cp,'tweet':tweet['tweet'], 'tweet_id':tweet['_id']})

    save_obj(candidate_presence, "Candidate")
    # into_new_db(candidate_presence)
    return candidate_presence


def filter_tweet_on_candidate(cname, tweet_list):
    return [tweet for tweet in tweet_list if tweet['cand_ana'][cname] != -1]






