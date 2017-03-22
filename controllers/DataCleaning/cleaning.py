import re
from controllers.DataCleaning import preprocessing
from functools import reduce
from DBModels.Username import *
import os
import time
# import preprocessor as p
from DBModels.Tweet import *
from controllers.DataCleaning import Patterns as pat
from controllers.Feature_Extraction import ngram_extractor
import pandas as pd

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


def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8', keep_default_na=False)


def expand_contractions(text, c_re=c_re):
    def replace(match):
        return dictionary[match.group(0)]
    return c_re.sub(replace, text)

def get_usernames(tweet_list):
    pattern = re.compile("@[a-zA-Z0-9]+")
    found_username_list = []

    for l in tweet_list:
        temp = []
        for m in [pattern.findall(l)]:
            temp.extend(m)
        found_username_list.append(temp)

    return found_username_list

def data_cleaning (tweet, nameTuple):
    # print ("Before:"+ tweet)
    # data anonymization
    tweet = reduce(lambda a, kv: a.replace(*kv), nameTuple, tweet)
    # removes URL, hashtags, and Reserved words
    # tweet = p.clean(tweet)
    tweet = pat.remove_from_tweet(tweet)
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

    # standardize words # collapse to 1 letter ex: cooool to col
    # tweet = ''.join(ch for ch, _ in itertools.groupby(tweet))

    # standardize words # collapse to 2 letter ex: cooool to cool
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


def process_hashtags(hashtag_list):
    pattern = re.compile("^\s+|\s*,\s*|\s+$")
    return [pattern.split(hashtags) if hashtags is not '' else [] for hashtags in hashtag_list]


def cleaning_file(fname):
    data_source = read_xlsx(fname)
    # add usernames to DB
    preprocessing.process_usernames(data_source)
    nameTuple = get_all_username_tup()

    raw_tweets = data_source['Tweet']
    cleaned_tweets = []
    [cleaned_tweets.append(data_cleaning(t, nameTuple)) for t in raw_tweets]

    unigrams, bigrams, trigrams = ngram_extractor.get_ngrams(cleaned_tweets)

    d = {'idTweet': data_source['Id'], 'idUsername': anonymize_poster_username(data_source['Username']),'tweet': cleaned_tweets, 'date_created': data_source['Date Created'], 'location':data_source['Location'], 'hashtags': process_hashtags(data_source['Hashtags']), 'favorite':data_source['Favorites'], 'retweet':data_source['Retweets'], 'users_mentioned':get_usernames(cleaned_tweets), 'unigram':unigrams, 'bigram':bigrams, 'trigram':trigrams}

    df = pd.DataFrame(data=d, index=None)
    # df.to_excel("CleanedTweets.xlsx", index=False)
    print("done cleaning")
    insert_new_tweet(df.to_dict(orient='records'))


# file_name = "C:\\Users\\Regina\\Google Drive\\Thesis\\Dummy Data\\test1.xlsx"
# data_source = read_xlsx(file_name)
# raw_tweets = data_source['Tweet']
# print(get_usernames(raw_tweets))


# start = time.time()
# cleaning_file(file_name)
# end = time.time()
# print(end - start)