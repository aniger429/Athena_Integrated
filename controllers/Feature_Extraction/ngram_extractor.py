import nltk
from nltk.util import ngrams
from DBModels.Tweet import *
import os
from controllers.DataCleaning import Patterns as pat

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "Lexicon_Files")
nltk.data.path.append(script_path+"/Lexicon_Files")


def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8', keep_default_na=False)


def get_ngrams(tweet_list):
    gramDict = dict()
    unigram_list = []
    bigram_list = []
    trigram_list = []
    final_list = []

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

        # gramDict['bigram'] = bigram
        # gramDict['trigram'] = trigram
        # final_list.append(copy.deepcopy(gramDict))
        # gramDict.clear()

    return unigram_list, bigram_list, trigram_list


# dum_data = get_tweets_only()
# unigrams, bigrams, trigrams = get_ngrams(dum_data)
# # df_output = pd.DataFrame.from_dict(output)
# # df_output.to_excel("feprocessed.xlsx", index=False, header=['Unigram', 'Bigram', 'Trigram'])
#
# for uni in unigrams:
#     print (uni)