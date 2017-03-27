from fuzzywuzzy import fuzz
from controllers.DataCleaning.Patterns import *
from controllers.analysis_controller.Pickle_Saver import *


def find_topic_tweets(topics_dict,tweets):
    print(topics_dict)
    for key, value in topics_dict.items():
        topic_words = [w['word'] for w in value]

        topic_tweets = []
        for tweet in tweets:
            twords = remove_usernames(tweet['tweet'])

            if fuzz.token_sort_ratio(twords,topic_words) >= 30:
                # tweet = {'tweet':tweet['tweet'], '_id':tweet['_id']}
                topic_tweets.append(tweet)

        topics_dict[key] = {'topic_tweets':topic_tweets, 'words': value}

    save_obj(topics_dict, "Topics")
    return topics_dict
