from nltk.util import ngrams

from controllers.DataCleaning import Patterns as pat


def get_ngrams(tweet_list):
    unigram_list = []
    bigram_list = []
    trigram_list = []

    # tweet = p.clean(tweet)
    tweet_list = [pat.remove_usernames(tweet) for tweet in tweet_list]

    for tweet in tweet_list:
        # splits the tweet into words
        tokens = tweet.split()

        uni = ngrams(tokens, 1)
        unigram = [' '.join(words) for words in uni]
        bi = ngrams(tokens, 2)
        bigram = [' '.join(words) for words in bi]
        tri = ngrams(tokens, 3)
        trigram = [' '.join(words) for words in tri]

        unigram_list.append(unigram)
        bigram_list.append(bigram)
        trigram_list.append(trigram)

    return unigram_list, bigram_list, trigram_list
