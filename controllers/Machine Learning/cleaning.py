import preprocessor as p
import pandas as pd
import re
import itertools
from functools import reduce
from DBModels.Username import *


stopwords = pd.read_csv("C:/Users/HKJ/AppData/Local/Programs/Python/Python35/Data Cleaning/Stopwords/eng-function-word.txt", header=None)
stopwords = stopwords.append(pd.read_csv("C:/Users/HKJ/AppData/Local/Programs/Python/Python35/Data Cleaning/Stopwords/fil-function-words.txt", header=None))
stopwords = stopwords[0].tolist()
stopwords = [x.lower() for x in stopwords]
stopwords = [re.sub('\'|"| ', '', x) for x in stopwords]

contractions = pd.read_csv("C:/Users/HKJ/AppData/Local/Programs/Python/Python35/Data Cleaning/Stopwords/contractions.csv", header=None, delimiter=',')
dictionary = dict(zip(contractions[0].tolist(), contractions[1].tolist()))

c_re = re.compile('(%s)' % '|'.join(dictionary.keys()))

nameTuple = getAllUsernames()

def readXLSX(filename):
    return pd.read_excel(filename)

def expandContractions(text, c_re=c_re):
    def replace(match):
        return dictionary[match.group(0)]
    return c_re.sub(replace, text)

def dataCleaning (tweet):
    #print ("Before:"+ tweet)
    #data anonymization
    tweet = reduce(lambda a, kv: a.replace(*kv), nameTuple, tweet)
    # removes URL, hashtags, and Reserved words
    p.set_options(p.OPT.URL, p.OPT.HASHTAG, p.OPT.RESERVED)
    tweet = p.clean(tweet)
    # remove HTML characters
    tweet = re.sub("(&\S+;)",'', tweet)
    # converts the tweets to lowercase
    tweet = tweet.lower()
    #expand contradictions
    tweet = expandContractions(tweet)
    # remove stopwords
    tweet = ' '.join([word for word in tweet.split() if word not in stopwords])
    #remove shortwords 1-2 characters
    shortword = re.compile(r'\W*\b\w{1,2}\b')
    tweet = shortword.sub('', tweet)
    # remove punctuation marks
    tweet = re.sub("(!|#|\$|%|\^|&|\*|\(|\)|\?|\.|,|\"|'|\+|=|\||\/|-|_|:|;)", '', tweet)
    #standardize words # collapse to 1
    tweet = ''.join(ch for ch, _ in itertools.groupby(tweet))
    # standardize words # collapse to 2
    # tweet = re.sub(r'(.)\1+', r'\1\1', tweet)

    #print("After:"+ tweet)

    return tweet

def cleaning(file_name):
    data = readXLSX(file_name)
    rawTweets = data['Tweet']
    cleanedTweets = []
    [cleanedTweets.append(dataCleaning(t)) for t in rawTweets[:10]]

file_name = "C:/Users/HKJ/AppData/Local/Programs/Python/Python35/Data Cleaning/Election-18.xlsx"

#cleaning(file_name)
