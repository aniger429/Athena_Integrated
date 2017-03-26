from afinn import Afinn
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import pandas as pd
import os

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "Lexicon_Files")
nltk.data.path.append(script_path+"/Lexicon_Files")

afinn = Afinn()
posiFile = pd.read_csv(file_path + "/positive.txt", header=None)
posi_list = posiFile[0].tolist()

nega_file = pd.read_csv(file_path + "/negative.txt", header=None)
nega_list = nega_file[0].tolist()

fil_words = pd.read_excel(file_path + "/fil_words_senti.xlsx", index_col='word')
fil_dict = fil_words.to_dict(orient='index')


def compute_filscore(tweet):
    # print("fil_score")
    # score = [fil_dict.get(w, {}).get('negativity',0) + fil_dict.get(w, {}).get('positivity',0) for w in tweet.split()]
    # print(score)
    return sum([fil_dict.get(w, {}).get('negativity',0) + fil_dict.get(w, {}).get('positivity',0) for w in tweet.split()])


def compute_afinn_score(tweet):
    # print("afinn")
    # score = [afinn.score(w) for w in tweet.split()]
    # print(score)
    return sum([afinn.score(w) for w in tweet.split()])


def compute_bing_score(tweet):
    # print("bing")
    # score = [1 if w in posi_list else -1 if w in nega_list else 0 for w in tweet.split()]
    # print(score)
    return sum([1 if w in posi_list else -1 if w in nega_list else 0 for w in tweet.split()])


def compute_sentiment(tweet):
    # print('Processing Sentiment Analysis for the word..')
    filScore = compute_filscore(tweet)
    afinnScore = compute_afinn_score(tweet)
    bingScore = compute_bing_score(tweet)

    """
    sip = swn.senti_synsets(aa)
    sipList = list(sip)
    if len(sipList) > 0:
        for i in range(0, len(sipList)):
            pos += sipList[i].pos_score()
            neg += sipList[i].neg_score()
    """
    final_score = bingScore + filScore + afinnScore

    return ["POSITIVE" if final_score > 0.0 else "NEGATIVE" if final_score < 0.0 else "NEUTRAL"]


def compute_tweets_sentiment(tweet_list):
    return [compute_sentiment(tweet) for tweet in tweet_list]

# print (compute_sentiment("i super hate banana"))

