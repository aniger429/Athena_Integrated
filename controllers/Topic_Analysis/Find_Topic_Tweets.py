from fuzzywuzzy import fuzz

from controllers.Pickles.Pickle_Saver import *


def find_topic_tweets(topics_dict, tweets):
    for key, value in topics_dict.copy().items():
        topic_words = ' '.join([w['word'] for w in value])
        topic_tweets_id = []
        for key1, tweet in tweets.iterrows():
            if fuzz.token_set_ratio(tweet['tweet'], topic_words) >= 35:
                topic_tweets_id.append(tweet['_id'])

        topic_tweets = tweets[tweets['_id'].isin(topic_tweets_id)]
        topics_dict[key] = {'topic_tweets': topic_tweets, 'words': value}

    save_obj(topics_dict, "Topics")
    return topics_dict
