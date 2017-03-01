import pandas as pd
import re
import itertools
from controllers.DataCleaning import preprocessing
from functools import reduce
from DBModels.Username import *
import os
import time
import preprocessor as p
from DBModels.Tweet import *


script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "stop_words")

stopwords = pd.read_csv(file_path+"/eng-function-word.txt", header=None)
stopwords = stopwords.append(pd.read_csv(file_path+"/fil-function-words.txt", header=None))
stopwords = stopwords[0].tolist()
stopwords = [x.lower() for x in stopwords]
stopwords = [re.sub('\'|"| ', '', x) for x in stopwords]

contractions = pd.read_csv(file_path+"/contractions.csv", header=None, delimiter=',')
dictionary = dict(zip(contractions[0].tolist(), contractions[1].tolist()))

c_re = re.compile('(%s)' % '|'.join(dictionary.keys()))

nameTuple = get_all_username_tup()
p.set_options(p.OPT.URL, p.OPT.HASHTAG, p.OPT.RESERVED, p.OPT.EMOJI)

def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8')


def expand_contractions(text, c_re=c_re):
    def replace(match):
        return dictionary[match.group(0)]
    return c_re.sub(replace, text)


def data_cleaning (tweet):
    # print ("Before:"+ tweet)
    # data anonymization
    tweet = reduce(lambda a, kv: a.replace(*kv), nameTuple, tweet)
    # removes URL, hashtags, and Reserved words
    tweet = p.clean(tweet)
    # remove HTML characters
    tweet = re.sub("(&\S+;)",'', tweet)
    # converts the tweets to lowercase
    tweet = tweet.lower()
    # expand contradictions
    tweet = expand_contractions(tweet)
    # remove stopwords
    tweet = ' '.join([word for word in tweet.split() if word not in stopwords])
    # remove shortwords 1-2 characters
    shortword = re.compile(r'\W*\b\w{1,2}\b')
    tweet = shortword.sub('', tweet)
    # remove punctuation marks
    tweet = re.sub("(!|#|\$|%|\^|&|\*|\(|\)|\?|\.|,|\"|'|\+|=|\||\/|-|_|:|;)", '', tweet)
    # standardize words # collapse to 1
    tweet = ''.join(ch for ch, _ in itertools.groupby(tweet))
    # standardize words # collapse to 2
    # tweet = re.sub(r'(.)\1+', r'\1\1', tweet)

    # print("After:"+ tweet)

    return tweet

def anonymize_poster_username(username_list):
    username_dict = get_all_username_dict()
    return [username_dict['@'+u] for u in username_list]

def write_csv(filename, cleanedTweets):
    # out = csv.writer(open("/home/dudegrim/Documents/"+filename, "w"), delimiter='\r')
    # out.writerow(cleanedTweets)
    script_path = os.path.dirname(__file__)
    directoryPath = os.path.join(script_path, filename)
    cleanedTweets.to_excel(excel_writer="/home/dudegrim/Documents/"+filename, index=False, header=None, encoding="utf-8")


def cleaning_file(fname):
    data_source = read_xlsx(fname)
    # add usernames to DB
    preprocessing.process_usernames(data_source)

    raw_tweets = data_source['Tweet']
    cleaned_tweets = []
    [cleaned_tweets.append(data_cleaning(t)) for t in raw_tweets]

    d = {'idTweet': data_source['Id'], 'idUsername': anonymize_poster_username(data_source['Username']),
         'tweet': cleaned_tweets,
         'date_created': data_source['Date Created']}

    df = pd.DataFrame(data=d, index=None)
    # df.to_excel("CleanedTweets.xlsx", index=False, header=['Tweets', 'Date Created', 'idTweet', 'idUsername'])

    insert_new_tweet(df.to_dict(orient='records'))


# file_name = "/home/dudegrim/Google Drive/Thesis/Election Data/Election-18.xlsx"
#
# start = time.time()
# test(file_name)
# end = time.time()
# print(end - start)