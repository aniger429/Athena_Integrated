from DBModels.KB_Names import *
from DBModels.Tweet import *


def identify_candidate(tweet_list):
    # gets all the known candidate names in the database
    candidate_names = get_all_kb_names()
    # stores a dictionary, key: tweet_id, value: dictionary of tweet_cp
    candidate_presence = {}

    for tweet in tweet_list:
        # key: candidate name, value: position of candidate name in a tweet, -1 for none
        tweet_cp = {}
        # for each candidate
        for candidate in candidate_names:
            tweet_cp[candidate['candidate_name']] = next((tweet['tweet'].index(word) for word in tweet['tweet'] if any(name in word for name in candidate['kb_names'])), -1)
              # tweet_cp[candidate['candidate_name']] = ([tweet['tweet'].index(word) for word in tweet['tweet'] if any(name in word for name in candidate['kb_names'])])

        candidate_presence[tweet['_id']] = tweet_cp
        # into_new_db(candidate_presence)

    return candidate_presence


# tweet_list = get_all_tweets()
# start = time.time()
# results = identify_candidate(tweet_list)
# end = time.time()
# print(end - start)
#
# print ("results")
# for key, value in results.items():
#     print (key)
#     print (value)



