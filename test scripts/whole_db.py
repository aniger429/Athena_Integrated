from DBModels.KB_Names import *
from controllers.DataCleaning import Patterns as pat
from controllers.Sentiment_Analysis.Sentiment_Identification import *

num_partitions = 6  # number of partitions to split dataframe
num_cores = 6  # number of cores on your machine
columns = ['Tweet', 'binay', 'duterte', 'poe', 'roxas', 'santiago']

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "controllers", "stop_words")

# loads stop words list from file
stopwords = pd.read_csv(file_path + "/final_stop_words_list.csv", header=None, squeeze=True).tolist()
# loads contractions from file
contractions = pd.read_csv(file_path + "/contractions.csv", header=None, delimiter=',')
dictionary = dict(zip(contractions[0].tolist(), contractions[1].tolist()))

c_re = re.compile('(%s)' % '|'.join(dictionary.keys()))

# path for classifiers
s_path = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(s_path, "controllers", "Pickles", "ML_Classifier")

# load pickled classififer
with open(os.path.join(path, 'LSVC.pkl'), 'rb') as fid:
    lscv_clf = pickle.load(fid)


def read_csv(filename):
    return pd.read_csv(filename, encoding="utf8", keep_default_na=False, index_col=None,
                       sep=",", skipinitialspace=True, usecols=['Tweet'], chunksize=100000)


def get_mention_index(tweet, candidate_names):
    # returns the position of the names used for the candidate in the tweet,
    # if candidate was not mentioned -1 is returned

    index = next((tweet.index(word) for word in tweet if any(name in word
                                                             for name in candidate_names)), -1)
    return index


def process_df(candidate_data, tweet_df):
    for candidate in candidate_data:
        tweet_df[candidate['candidate_name']] = tweet_df.apply(lambda row: get_mention_index(row['tweet_cleaned'],
                                                                                             candidate['kb_names']),
                                                               axis=1)
    return tweet_df


def lower_split_tweet(tweet):
    return tweet.lower().split(' ')


def identify_candidate(candidate_data, tweet_df):
    # convert all tweets to list of words
    # if isinstance(tweet_df['Tweet'].iloc[0], list):
    #     tweet_df['Tweet'] = tweet_df.apply(lambda row: row['Tweet'], axis=1)
    # else:
    #     tweet_df['tweet_cleaned'] = tweet_df.apply(lambda row: lower_split_tweet(row['tweet_cleaned']), axis=1)

    # creates a new column per candidate and stores the index of word mentioned for the candidate
    # tweet_df = parallelize_dataframe(tweet_df, process_df, candidate_data)

    tweet_df = process_df(candidate_data, tweet_df)

    return tweet_df


def parallelize_chunk(chunk, func, candidate_data):
    df_split = np.array_split(chunk, num_partitions)
    pool = Pool(num_cores)
    func = partial(func, candidate_data)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def find_more_names(tweets):
    candidate_names = get_all_kb_names()
    results = {}

    for candidate in candidate_names:
        l1 = [word for tweet in tweets for word in tweet if any(name in word for name in candidate['kb_names'])]
        l1_unique = list(set(l1))
        l1_final = [x for x in l1_unique if x not in candidate['blacklist_names']]

        results[candidate['candidate_name']] = l1_final

    # for candidate in candidate_names:
    #     results[candidate['candidate_name']] = list(set([word for tweet in tweets for word in tweet
    #                                                      if any(name in word for name in candidate['kb_names'])
    #                                                      and (word not in candidate['blacklist_names'])]))

    kb_names_update(results)


def write_csv(filename, tweets):
    import os
    # if file does not exist write header
    if not os.path.isfile(filename):
        return tweets.to_csv(filename, header=True, sep=',', columns=columns, index=False, chunksize=10000)
    else:  # else it exists so append without writing the header
        return tweets.to_csv(filename, mode='a', sep=',', columns=columns, index=False, header=False, chunksize=10000)


def write_data(filename, data):
    import os
    # if file does not exist write header
    if not os.path.isfile(filename):
        return data.to_csv(filename, header=True, sep=',', index=False)
    else:  # else it exists so append without writing the header
        return data.to_csv(filename, mode='a', sep=',', index=False, header=False)


def expand_contractions(text, c_re=c_re):
    def replace(match):
        return dictionary[match.group(0)]

    return c_re.sub(replace, text)


def init_data_cleaning(tweet):
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

    # return tweet.split(' ')
    return tweet


def cleaning(df):
    df['tweet_cleaned'] = df.apply(lambda row: init_data_cleaning(row['Tweet']), axis=1)
    return df


def parallelize_cleaning(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def start_process(file_name):
    filepath = "/home/dudegrim/Documents/CSV8/"

    print("Start", file_name)
    reader = read_csv(filepath + file_name)
    results = pd.DataFrame()

    # gets all the known candidate names in the database
    candidate_data = get_all_kb_names()

    for ctr, chunk1 in enumerate(reader):
        # add usernames to DB
        cleaned = parallelize_cleaning(chunk1, cleaning)
        results = parallelize_chunk(cleaned, identify_candidate, candidate_data)
        # this removes empty tweets after cleaning
        results.drop(results[results.tweet_cleaned == ""].index, inplace=True)

        # find_more_names(results["tweet_cleaned"])

        cand_count = {}
        for candidate in candidate_data:
            cand_df = results[results[candidate['candidate_name']] >= 0]

            cand_count[candidate['candidate_name']] = len(cand_df)
            # save the stuff
            write_csv("/home/dudegrim/Documents/whole/" + candidate['candidate_name'] + ".csv", cand_df)

        data_count = pd.DataFrame(cand_count, index=[0])

        write_data("/home/dudegrim/Documents/whole/candidate_data_count.csv", data_count)

    return


def bitch_file():
    filepath = "/home/dudegrim/Documents/CSV8/Election-13.csv"

    print("Start", "Bitch")
    reader = read_csv(filepath)
    results = pd.DataFrame()

    # gets all the known candidate names in the database
    candidate_data = get_all_kb_names()

    for ctr, chunk1 in enumerate(reader):

        chunk1['tweet_cleaned'] = [init_data_cleaning(row['Tweet']) for key, row in chunk1.iterrows()]
        results = parallelize_chunk(chunk1, identify_candidate, candidate_data)
        # this removes empty tweets after cleaning
        results.drop(results[results.tweet_cleaned == ""].index, inplace=True)

        # find_more_names(results["tweet_cleaned"])

        cand_count = {}
        for candidate in candidate_data:
            cand_df = results[results[candidate['candidate_name']] >= 0]

            cand_count[candidate['candidate_name']] = len(cand_df)
            # save the stuff
            write_csv("/home/dudegrim/Documents/whole/" + candidate['candidate_name'] + ".csv", cand_df)

        data_count = pd.DataFrame(cand_count, index=[0])

        write_data("/home/dudegrim/Documents/whole/candidate_data_count.csv", data_count)

    return


def lscv_sentiment(tweet_list):
    # predict sentiment of tweet
    return lscv_clf.predict(tweet_list)


def read_csv_sentiment(filename):
    print(filename)
    return pd.read_csv(filename, encoding="utf8", keep_default_na=False, index_col=None,
                       sep=",", skipinitialspace=True, usecols=columns, chunksize=100000, engine='python')


def process_sentiment():
    filepath = "/home/dudegrim/Documents/whole/"

    results = pd.DataFrame()

    # gets all the known candidate names in the database
    candidate_data = get_all_kb_names()

    for cand in candidate_data:
        reader = read_csv_sentiment(filepath + cand['candidate_name'] + ".csv")

        for ctr, chunk1 in enumerate(reader):
            chunk1['tweet_cleaned'] = chunk1.apply(lambda row: init_data_cleaning(row['Tweet']), axis=1)
            chunk1['sentiment'] = lscv_sentiment(chunk1['tweet_cleaned'])

            positive_tweets = chunk1.loc[chunk1['sentiment'] == "Positive"]
            neutral_tweets = chunk1.loc[chunk1['sentiment'] == "Neutral"]
            negative_tweets = chunk1.loc[chunk1['sentiment'] == "Negative"]

            write_csv("/home/dudegrim/Documents/whole/Sentiment/positive_tweets_" + cand['candidate_name'] + ".csv",
                      positive_tweets)
            write_csv("/home/dudegrim/Documents/whole/Sentiment/neutral_tweets_" + cand['candidate_name'] + ".csv",
                      neutral_tweets)
            write_csv("/home/dudegrim/Documents/whole/Sentiment/negative_tweets_" + cand['candidate_name'] + ".csv",
                      negative_tweets)

            data_count = pd.DataFrame({'Positive': len(positive_tweets), 'Neutral': len(neutral_tweets),
                                       'Negative': len(negative_tweets)}, index=[0])

            write_data("/home/dudegrim/Documents/whole/Sentiment/data_count_" + cand['candidate_name'] + ".csv",
                       data_count)


# start = time.time()
# process_sentiment()
# end = time.time()
# print(end-start)

# for r in range(14, 18, 1):
#     print(r)
#     start = time.time()
#     start_process("Election-"+str(r)+".csv")
#     end = time.time()
#     print(end-start)
# bitch_file()


process_sentiment()
