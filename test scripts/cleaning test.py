import re
from controllers.DataCleaning import preprocessing
from functools import reduce
from DBModels.Username import *
import os
# import preprocessor as p
from DBModels.Tweet import *
from controllers.DataCleaning import Patterns as pat
from controllers.Feature_Extraction import ngram_extractor
import pandas as pd

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "stop_words")

# loads stop words list from file
stopwords = pd.read_csv(file_path+"/final_stop_words_list.csv", header=None, squeeze=True).tolist()
# loads contractions from file
contractions = pd.read_csv(file_path+"/contractions.csv", header=None, delimiter=',')
dictionary = dict(zip(contractions[0].tolist(), contractions[1].tolist()))

c_re = re.compile('(%s)' % '|'.join(dictionary.keys()))


def read_csv(filename):
    return pd.read_csv(filename, encoding="utf8", keep_default_na=False, index_col=None,
                       sep=",", skipinitialspace=True, chunksize=1000)


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


def init_data_cleaning(tweet, nameTuple):
    # print ("Before:" + tweet)
    # data anonymization
    tweet = reduce(lambda a, kv: a.replace(*kv), nameTuple, tweet)
    # removes URL, hashtags, HTML, and Reserved words
    tweet = pat.remove_from_tweet(tweet)
    # converts the tweets to lowercase
    tweet = tweet.lower()
    # expand contradictions
    tweet = expand_contractions(tweet)

    split_tweet = tweet.split(' ')
    split_tweet = filter(None, split_tweet)

    # standardize words collapse to 2 letter ex: cooool to cool
    tweet = ' '.join([(re.sub(r'(.)\1+', r'\1\1', word)) if word[0] != '@' else word for word in split_tweet])

    # processes emoticons
    # positive
    tweet = re.sub("[:;8=x][-oc]*[>D)}P\]3]+", "POSEMOTE", tweet)
    tweet = re.sub("[<({\[]+[-o]*[:;8=x]", "POSEMOTE", tweet)

    tweet = re.sub("[:;8=x][-oc]*[<({\[]+", "NEGEMOTE", tweet)
    tweet = re.sub("[>D)}\]]+[-o]*[:;8=x]", "NEGEMOTE", tweet)

    # remove punctuation marks
    tweet = re.sub('[^A-Za-z0-9@ ]+', ' ', tweet)

    split_tweet = tweet.split(' ')

    # remove stopwords
    split_tweet = [word for word in split_tweet if word not in stopwords]

    # remove shortwords 1-2 characters
    split_tweet = [word for word in split_tweet if len(word) > 1]

    # remove extra spaces between words
    tweet = ' '.join(split_tweet)

    # print("After:" + tweet)

    return tweet

# # no username anonymization
# def data_cleaning (tweet):
#     tweet = pat.remove_from_tweet(tweet)
#     # remove HTML characters
#     tweet = re.sub("(&\S+;)",'', tweet)
#     # converts the tweets to lowercase
#     tweet = tweet.lower()
#     # expand contradictions
#     tweet = expand_contractions(tweet)
#     # remove stopwords
#     tweet = ' '.join([word for word in tweet.split() if word not in stopwords])
#     # remove shortwords 1-2 characters
#     shortword = re.compile(r'\W*\b\w{1,2}\b')
#     tweet = shortword.sub('', tweet)
#     # remove punctuation marks
#     tweet = re.sub("(!|#|\$|%|\^|&|\*|\(|\)|\?|\.|,|\"|'|\+|=|\||\/|-|_|:|;|\"|—|–|’|`|”|…|‘|“|”)", '', tweet)
#
#     # standardize words # collapse to 1 letter ex: cooool to col
#     # tweet = ''.join(ch for ch, _ in itertools.groupby(tweet))
#
#     # standardize words # collapse to 2 letter ex: cooool to cool
#     # tweet = re.sub(r'(.)\1+', r'\1\1', tweet)
#
#     # print("After:"+ tweet)
#
#     return tweet


def anonymize_poster_username(username_list):
    username_dict = get_all_username_dict()
    return [username_dict['@'+u] for u in username_list]


def process_hashtags(hashtag_list):
    pattern = re.compile("^\s+|\s*,\s*|\s+$")
    return [pattern.split(hashtags) if hashtags is not '' else [] for hashtags in hashtag_list]


def cleaning_file(file_name):
    print("Start Cleaning File")
    reader = read_csv(file_name)

    for ctr, chunk in enumerate(reader):
        # add usernames to DB
        preprocessing.process_usernames(chunk)
        nameTuple = get_all_username_tup()

        raw_tweets = chunk['Tweet']
        cleaned_tweets = []
        [cleaned_tweets.append(init_data_cleaning(t, nameTuple)) for t in raw_tweets]

        unigrams, bigrams, trigrams = ngram_extractor.get_ngrams(cleaned_tweets)

        # chunk['Tweet'] = chunk['Tweet'].apply(lambda x: preprocess(x))

        posemotecount = [tweet.count('POSEMOTE') for tweet in cleaned_tweets]
        negemotecount = [tweet.count('NEGEMOTE') for tweet in cleaned_tweets]

        d = {'idTweet': chunk['Id'], 'idUsername': anonymize_poster_username(chunk['Username']),
             'orig_tweets': raw_tweets, 'tweet': cleaned_tweets, 'date_created': chunk['Date Created'],
             'location': chunk['Location'],'hashtags': process_hashtags(chunk['Hashtags']),
             'favorite': chunk['Favorites'], 'retweet': chunk['Retweets'],
             'posemote': posemotecount,  'negemote': negemotecount,
             'users_mentioned': get_usernames(cleaned_tweets),
             'unigram': unigrams, 'bigram': bigrams, 'trigram': trigrams}

        df = pd.DataFrame(data=d, index=None)
        # this removes empty tweets after cleaning
        df.drop(df[df.tweet == ""].index, inplace=True)

        insert_new_tweet(df.to_dict(orient='records'))

    print("Done Cleaning File")