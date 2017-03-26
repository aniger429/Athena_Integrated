import csv
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from collections import defaultdict
import numpy as np
from nltk.text import TextCollection
from DBModels.Tweet import *
from controllers.DataCleaning.Patterns import *
import collections
from operator import itemgetter

tweetlist = []

"""
This function displays the output of Python's LDA. You may use this as a guide on how to display the topics with its
corresponding weights assigned by LDA
"""
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print(''.join([feature_names[i] + ' ' + str(topic[i]) + ' ' + ' + '
                       for i in topic.argsort()[:-no_top_words - 1:-1]]))

"""
This function reads the rows of a CSV file. It converts it csv row as a string. This is the only implementation of
extracting CSV rows into list that works for SCIKIT. Tweetlist is a LIST of String/Tweets.
"""
def get_Tweets(fileName):
    with open(fileName,'r',encoding='utf-8',errors= 'ignore') as input_file:
        csvreader = csv.reader(input_file, delimiter=',')
        for row in csvreader:
            tweetlist.append(" ".join(row))



"""
This function computes for the TFIDF values for NGRAMS using NLTK's TextCollection class. The variable self is an
instantiation of the TextCollection class which contains the corpus. It is passed to this function. How to use will be
enumerated below all functions. The variable ngrams should be a list containing all ngrams you want to weigh using TFIDF.
Outputs a dictionary that has all the ngrams as its key and their corresponding tfidf value as their value.
"""
def tfidf_ngrams(self,ngrams, tweets):
    tfidf_values = defaultdict(list)

    tfidf = 0
    num_docs = 0
    tf = 0
    tf_total = 0
    for ngram in ngrams:
        for tweet in tweets:
            #Summation of the TF of each term in all tweets
            tf = TextCollection.tf(self,ngram.lower(),tweet.lower())
            tf_total += tf
        #Computing for TFIDF
        tfidf = tf_total * TextCollection.idf(self,ngram.lower())
        tfidf_values[ngram].append(tfidf)

    return tfidf_values


"""
This function computes for the top n-grams from the Tweet corpus using SCIKIT. The variable start_range indicates the
lowest n-gram you would want it to produce. The variable end_range indicates the highest n-gram you would want it to
produce. If you want pure unigrams, then both range variables should be set to 1. The output finallist is a dictionary
that has ngrams as its key and the tfidf value as its value.
"""
def tfidf_vectorizer(tweets,start_range, end_range):
    tfidfvec = TfidfVectorizer(ngram_range=(start_range,end_range), min_df=0, use_idf=True, sublinear_tf=True,analyzer='word', norm= 'l1')
    z = tfidfvec.fit_transform(tweets)
    idf = tfidfvec.idf_
    ngramlist = tfidfvec.get_feature_names()
    ngramscore = np.asarray(z.sum(axis=0)).ravel()
    tf_idf_dict = dict(zip(ngramlist,ngramscore))
    finallist = collections.OrderedDict(sorted(tf_idf_dict.items(), key=itemgetter(1), reverse=True)[:100])
    return finallist


"""
This function performs the Latent Dirichlet Allocation (LDA) method on the tweet corpus. The implementation includes the
TFIDF value to generate the LDA weights. The variables start_range and end_range both correspond to the number of
ngrams you want to analyze. Pure unigrams would require 1,1 as value respectively and etc. The variables num_topics &
num_iter refer to the number of topics you want it to produce and number of iterations you want it to iterate through
each document.
"""
def topic_lda_tfidf(tweets, start_range,end_range, num_topics, num_iter):
    tfidfvec = TfidfVectorizer(ngram_range=(start_range, end_range), min_df=0, use_idf=True, sublinear_tf=True, norm='l2',
                               smooth_idf=True)
    z = tfidfvec.fit_transform(tweets)
    print("Topic Modeling")
    lda = LatentDirichletAllocation(n_topics=num_topics, max_iter=num_iter, learning_method='batch')
    # tweets.reshape(1, -1)
    lda.fit_transform(z)
    score = lda.score(z)

    no_top_words = 15
    feature_names = tfidfvec.get_feature_names()
    topics_dict= collections.OrderedDict()

    for topic_idx, topic in enumerate(lda.components_):
        words_list = list()
        for i in topic.argsort()[:-no_top_words - 1:-1]:
            words_list.append({'word':feature_names[i],'score':topic[i]})

        topics_dict[str(topic_idx+1)] = words_list

    return topics_dict


"""
This function performs the Latent Dirichlet Allocation (LDA) method on the tweet corpus The variables start_range and
end_range both correspond to the number of ngrams you want to analyze. Pure unigrams would require 1,1 as value respectively
and etc. The variables num_topics & num_iter refer to the number of topics you want it to produce and number of iterations
you want it to iterate through each document.
"""
def topic_lda(tweets, start_range,end_range, num_topics, num_iter):
    vectorizer = CountVectorizer(ngram_range=(start_range, end_range), encoding="utf-8", min_df=0)
    topic = vectorizer.fit_transform(tweets)

    lda = LatentDirichletAllocation(n_topics=num_topics, max_iter=num_iter, learning_method='batch')
    # tweets.reshape(1, -1)
    lda.fit_transform(topic)
    score = lda.score(topic)

    display_topics(lda, topic.get_feature_names(), 20)


"""
This function outputs the ngrams along with its corresponding TFIDF value into a CSV file.
"""
def write_to_csv(fileName, tweet_list):
    with open(fileName, 'w', encoding='utf-8', newline='') as input_file:
        csvwriter = csv.writer(input_file, delimiter=',')
        for ngram, value in tweet_list.items():
            csvwriter.writerow([ngram, value])



#How to use

#Getting the tweets
# get_Tweets('CleanedTweets.csv')
#Converting the list of tweets into an array since this is what scikit requires
# tweets = np.asarray(tweetlist)

# tweets = get_tweets_only()
# tweets = [remove_usernames(t) for t in tweets]
# final_list = tfidf_vectorizer(tweets,1,3)


# print("NGRAMS TFIDF")

#This is how you instantiate the TextCollection class. You pass to it the List of documents
# nltk = TextCollection(tweets)
# print(nltk)
# print(list(final_list.keys()))
# result = tfidf_ngrams(nltk,list(final_list.keys()), tweets)


# #Printing the ngram and tfidf score
# for keys,values in final_list.items():
#     print(keys,values)

#SCIKIT Functions, just pass the necessary parameters required by each function
# print("SCIKIT")
# write_to_csv('TextlistContents.csv',final_list)
# print("Done!")

# topic_lda_tfidf(tweets, 1, 1, 10, 100)