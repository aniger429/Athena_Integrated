import os
import pandas as pd

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "Lexicon_Files", "final_sentiment_words")


posEngFile = pd.read_csv(file_path + "/positive_sentiment_words_english.csv", skiprows=1, header=None)
posEng = posEngFile[0].tolist();

negEngFile = pd.read_csv(file_path + "/negative_sentiment_words_english.csv", skiprows=1, header=None)
negEng = negEngFile[0].tolist();

posFilFile = pd.read_csv(file_path + "/positive_sentiment_words_filipino.csv", skiprows=1, header=None)
posFil = posFilFile[0].tolist();

negFilFile = pd.read_csv(file_path + "/negative_sentiment_words_filipino.csv", skiprows=1, header=None)
negFil = negFilFile[0].tolist();

def tweet_words_positive(tweet):
    array = []
    splitter = tweet.split()
    for word in splitter:
        if (word in posEng) or (word in posFil):
            print(word + ': Positive')
            array.append(word)
    return array

def tweet_words_negative(tweet):
    array = []
    splitter = tweet.split()
    for word in splitter:
        if (word in negEng) or (word in negFil):
            print(word + ': Negative')
            array.append(word)
    return array   


a = tweet_words_positive('protistan is legally happy')
print(a)

