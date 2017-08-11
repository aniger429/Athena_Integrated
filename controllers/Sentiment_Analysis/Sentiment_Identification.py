from afinn import Afinn
import nltk
from controllers.Pickles.Pickle_Saver import *
from collections import Counter
from multiprocessing import Pool
from functools import partial
import numpy as np
import pickle
from DBModels.Lexicon import *
import re
num_partitions = 6  # number of partitions to split dataframe
num_cores = 6  # number of cores on your machine


# script_path = os.path.dirname(os.path.dirname(__file__))
# file_path = os.path.join(script_path, "Lexicon_Files")
# nltk.data.path.append(script_path+"/Lexicon_Files")
#
# afinn = Afinn(emoticons=True)
# posiFile = pd.read_csv(file_path + "/positive.txt", header=None)
# posi_list = posiFile[0].tolist()
#
# nega_file = pd.read_csv(file_path + "/negative.txt", header=None)
# nega_list = nega_file[0].tolist()
#
# fil_words = pd.read_excel(file_path + "/fil_words_senti.xlsx", index_col='word')
# fil_dict = fil_words.to_dict(orient='index')


# def compute_filscore(tweet):
#     return sum([fil_dict.get(word, {}).get('positivity', 0) - fil_dict.get(word, {}).get('negativity', 0)
#                 for word in tweet])
#
#
# def evaluate_score(score):
#     if score > 0:
#         return "POSITIVE"
#     elif score == 0:
#         return "NEUTRAL"
#     else:
#         return "NEGATIVE"
#
#
# def compute_afinn_score(tweet):
#     afinnScore = 0
#     afinnSum = 0
#     for word in tweet:
#         if (afinn.score(word) > 0) and (afinnScore < 0):  # N + P
#             afinnScore = 0
#             afinnScore -= afinn.score(word)
#         elif (afinn.score(word) < 0) and (afinnScore < 0):  # N + N
#             afinnScore = 0
#             afinnScore += (afinn.score(word) * -1)
#
#         elif (afinn.score(word) < 0) and (afinnScore > 0):  # P + N
#             afinnScoreAdd = afinnScore
#             afinnScore = 0
#             afinnScore += (-(afinnScoreAdd) + afinn.score(word))
#         else:  # P + P or else
#             afinnScore = 0
#             afinnScore += afinn.score(word)
#
#         afinnSum += afinnScore
#
#     if 'POSEMOTE' in tweet:
#         afinnSum += 1
#     elif 'NEGEMOTE' in tweet:
#         afinnSum -= 1
#
#     return afinnSum
#
#
# def compute_bing_score(tweet):
#     bingScore = 0
#     bingSum = 0
#     for word in tweet:
#         if (word in posi_list) and (bingScore < 0):  # N + P
#             bingScore = -2
#         elif (word in posi_list):  # P + P
#             bingScore = 1
#         else:
#             if (word in nega_list) and (bingScore > 0):  # P + N
#                 bingScore = -2
#             elif (word in nega_list) and (bingScore < 0):  # N + N (double negative)
#                 bingScore = 1
#             elif (word in nega_list):
#                 bingScore = -1
#             else:
#                 bingScore = 0
#
#         bingSum += bingScore
#
#     return bingSum
#
#
# def compute_sentiment(tweet):
#     filScore = evaluate_score(compute_filscore(tweet))
#     afinnScore = evaluate_score(compute_afinn_score(tweet))
#     bingScore = evaluate_score(compute_bing_score(tweet))
#
#     # print(' '.join(tweet)  + filScore + afinnScore + bingScore)
#     final_score = Counter([bingScore, filScore, afinnScore]).most_common()[0]
#
#     if final_score[1] == 1:
#         final = "NEUTRAL"
#     else:
#         final = final_score[0]
#
#     return final.lower()
#
#
# def lexicon_sentiment(tweet_list):
#     tweet_list['sentiment'] = tweet_list['tweet'].apply(lambda x: compute_sentiment(x.split(' ')).title())
#
#     return tweet_list

posEng = get_all_words("english", "positive")
negEng = get_all_words("english", "negative")
posFil = get_all_words("filipino", "positive")
negFil = get_all_words("filipino", "negative")


def lscv_sentiment(tweet_list):
    # path for classifiers
    s_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(s_path, "Pickles", "ML_Classifier")

    # load pickled classififer
    with open(os.path.join(path, 'LSVC.pkl'), 'rb') as fid:
        lscv_clf = pickle.load(fid)

    # predict sentiment of tweet
    return lscv_clf.predict(tweet_list)


def sa_parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def check_word(lex_list, word):
    return next((s for s in lex_list if word == s), "None")


def get_word_sentiment(tweet):
    # word_list = []
    # for word in tweet.split(' '):
    #     processed_word = re.sub('[^A-Za-z0-9@ ]+', '', word.lower())
    #     if (processed_word in negEng) or (processed_word in negFil):
    #         print(processed_word, "negative")
    #         word_list.append((word, 'negative'))
    #     elif (processed_word in posEng) or (processed_word in posFil):
    #         print(processed_word, "positive")
    #         word_list.append((word, 'positive'))
    #     else:
    #         print(processed_word, "neutral")
    #         word_list.append((word, 'neutral'))
    #
    # return word_list
    word_list = []
    for word in tweet.split(' '):
        processed_word = re.sub('[^A-Za-z0-9@ ]+', '', word.lower())
        check_neg_eng = check_word(negEng, processed_word)
        check_neg_fil = check_word(negFil, processed_word)
        check_pos_eng = check_word(posEng, processed_word)
        check_pos_fil = check_word(posFil, processed_word)
        if check_neg_eng != "None":

            word_list.append({"word": word, "sentiment": "negative", "language": "english", "matched": check_neg_eng})
        elif check_pos_eng != "None":
            word_list.append({"word": word, "sentiment": "positive", "language": "english", "matched": check_pos_eng})
        elif check_neg_fil != "None":
            word_list.append({"word": word, "sentiment": "negative", "language": "filipino", "matched": check_neg_fil})
        elif check_pos_fil != "None":
            word_list.append({"word": word, "sentiment": "positive", "language": "filipino", "matched": check_pos_fil})
        else:
            word_list.append({"word": word, "sentiment": "neutral", "language": "", "matched": ""})
    return word_list


def compute_tweets_sentiment(tweet_list):
    # Lexicon Based
    # tweet_list = sa_parallelize_dataframe(tweet_list, lexicon_sentiment)
    # returns a list of all the words with their corresponding sentiment
    tweet_list['words_senti'] = tweet_list.apply(lambda row: get_word_sentiment(row['orig_tweets']), axis=1)
    # Machine Learning - LSVC
    tweet_list['sentiment'] = lscv_sentiment(tweet_list['tweet'])
    posi_tweets = tweet_list[tweet_list['sentiment'] == "Positive"]
    neut_tweets = tweet_list[tweet_list['sentiment'] == "Neutral"]
    neg_tweets = tweet_list[tweet_list['sentiment'] == "Negative"]

    columns = ['orig_tweets', '_id', 'tweet', 'sentiment']
    # Select the ones you want
    save_dataframe(posi_tweets.loc[:, columns], 'positive')
    save_dataframe(neut_tweets.loc[:, columns], 'neutral')
    save_dataframe(neg_tweets.loc[:, columns], 'negative')

    return posi_tweets, neut_tweets, neg_tweets


