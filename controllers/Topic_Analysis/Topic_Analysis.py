import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
import numpy as np
from nltk.text import TextCollection
import collections
from operator import itemgetter
from sklearn.manifold import TSNE
import simplejson as json
import os
tweetlist = []

"""
This function displays the output of Python's LDA. You may use this as a guide on how to display the topics with its
corresponding weights assigned by LDA
"""


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(''.join([feature_names[i] + ' ' + str(topic[i]) + ' ' + ' + '
                       for i in topic.argsort()[:-no_top_words - 1:-1]]))


"""
This function reads the rows of a CSV file. It converts it csv row as a string. This is the only implementation of
extracting CSV rows into list that works for SCIKIT. Tweetlist is a LIST of String/Tweets.
"""


def get_Tweets(fileName):
    with open(fileName, 'r', encoding='utf-8', errors='ignore') as input_file:
        csvreader = csv.reader(input_file, delimiter=',')
        for row in csvreader:
            tweetlist.append(" ".join(row))


"""
This function computes for the TFIDF values for NGRAMS using NLTK's TextCollection class. The variable self is an
instantiation of the TextCollection class which contains the corpus. It is passed to this function. How to use will be
enumerated below all functions. The variable ngrams should be a list containing all ngrams you want to weigh using TFIDF.
Outputs a dictionary that has all the ngrams as its key and their corresponding tfidf value as their value.
"""


def tfidf_ngrams(self, ngrams, tweets):
    tfidf_values = defaultdict(list)

    tfidf = 0
    num_docs = 0
    tf = 0
    tf_total = 0
    for ngram in ngrams:
        for tweet in tweets:
            # Summation of the TF of each term in all tweets
            tf = TextCollection.tf(self, ngram.lower(), tweet.lower())
            tf_total += tf
        # Computing for TFIDF
        tfidf = tf_total * TextCollection.idf(self, ngram.lower())
        tfidf_values[ngram].append(tfidf)

    return tfidf_values


"""
This function computes for the top n-grams from the Tweet corpus using SCIKIT. The variable start_range indicates the
lowest n-gram you would want it to produce. The variable end_range indicates the highest n-gram you would want it to
produce. If you want pure unigrams, then both range variables should be set to 1. The output finallist is a dictionary
that has ngrams as its key and the tfidf value as its value.
"""


def tfidf_vectorizer(tweets, start_range, end_range):
    tfidfvec = TfidfVectorizer(ngram_range=(start_range, end_range), min_df=0, use_idf=True, sublinear_tf=True,
                               analyzer='word', norm='l1')
    z = tfidfvec.fit_transform(tweets)
    idf = tfidfvec.idf_
    ngramlist = tfidfvec.get_feature_names()
    ngramscore = np.asarray(z.sum(axis=0)).ravel()
    tf_idf_dict = dict(zip(ngramlist, ngramscore))
    finallist = collections.OrderedDict(sorted(tf_idf_dict.items(), key=itemgetter(1), reverse=True)[:100])
    return finallist


"""
This function performs the Latent Dirichlet Allocation (LDA) method on the tweet corpus. The implementation includes the
TFIDF value to generate the LDA weights. The variables start_range and end_range both correspond to the number of
ngrams you want to analyze. Pure unigrams would require 1,1 as value respectively and etc. The variables num_topics &
num_iter refer to the number of topics you want it to produce and number of iterations you want it to iterate through
each document.
"""


def topic_lda_tfidf(tweets, start_range, end_range, num_topics, num_iter, no_top_words=15):
    tfidfvec = TfidfVectorizer(ngram_range=(start_range, end_range),
                               min_df=0, use_idf=True,
                               sublinear_tf=True,
                               norm='l2',
                               smooth_idf=True)
    z = tfidfvec.fit_transform(tweets)
    lda = LatentDirichletAllocation(n_topics=num_topics, max_iter=num_iter,
                                    learning_method='online')
    # tweets.reshape(1, -1)
    lda.fit_transform(z)
    score = lda.score(z)

    # no_top_words = 15
    feature_names = tfidfvec.get_feature_names()
    topics_dict = collections.OrderedDict()

    for topic_idx, topic in enumerate(lda.components_):
        words_list = list()
        for i in topic.argsort()[:-no_top_words - 1:-1]:
            words_list.append({'word': feature_names[i], 'score': topic[i]})

        topics_dict[str(topic_idx + 1)] = words_list

    return topics_dict


def testing_pylda(tweets):
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    stop_words='english',
                                    lowercase=True,
                                    token_pattern=r'\b[a-zA-Z]{3,}\b',
                                    max_df=0.5,
                                    min_df=10)
    # dtm_tf = tf_vectorizer.fit_transform(tweets)

    tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
    dtm_tfidf = tfidf_vectorizer.fit_transform(tweets)

    # for TF DTM
    # lda_tf = LatentDirichletAllocation(n_topics=20, random_state=0)
    # lda_tf.fit(dtm_tf)
    # for TFIDF DTM
    lda_tfidf = LatentDirichletAllocation(n_topics=10, random_state=0)
    lda_tfidf.fit(dtm_tfidf)

    return lda_tfidf, dtm_tfidf, tfidf_vectorizer


"""
This function performs the Latent Dirichlet Allocation (LDA) method on the tweet corpus The variables start_range and
end_range both correspond to the number of ngrams you want to analyze. Pure unigrams would require 1,1 as value respectively
and etc. The variables num_topics & num_iter refer to the number of topics you want it to produce and number of iterations
you want it to iterate through each document.
"""


def topic_lda(tweets, start_range, end_range, num_topics, num_iter):
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


def topic_analysis_lda(tweets, start_range, end_range, num_topics, num_iter, no_top_words=15):
    tfidfvec = TfidfVectorizer(ngram_range=(start_range, end_range),
                               min_df=5, use_idf=True,
                               sublinear_tf=True,
                               norm='l2',
                               smooth_idf=True, stop_words='english')
    cvz = tfidfvec.fit_transform(tweets)
    # train an LDA model
    lda_model = LatentDirichletAllocation(n_topics=num_topics, max_iter=num_iter,
                                          learning_method='batch')
    # tweets.reshape(1, -1)
    lda_model.fit_transform(cvz)
    score = lda_model.score(cvz)

    # no_top_words = 15
    feature_names = tfidfvec.get_feature_names()
    topics_dict = collections.OrderedDict()

    for topic_idx, topic in enumerate(lda_model.components_):
        words_list = list()
        for i in topic.argsort()[:-no_top_words - 1:-1]:
            words_list.append({'word': feature_names[i], 'score': topic[i]})

        topics_dict[str(topic_idx + 1)] = words_list

    # insert JSON file processing
    json_string = {}  # This is the final json string to be written on a json file
    links = []  # The list that will contain all the links
    nodes = []  # The list that will contan all the nodes

    topic_cnt = 0  # Index pertaining to the topic number of a certain node
    topic_node = False  # Boolean that is responsible for telling if a certain index is a topic node
    destination_num = 2  # Pertains to the destination index. Starts at 2 because node 0 = root node,
    # 1 = topic node 1, node 2 is the start of word nodes
    dict_count = 0  # Index to iterate the topic_dict
    count = 0  # Counter for the number of words to initialize
    node_cnt = 0  # Index to pertain to the current number of topic nodes initialized

    # First node initialization
    node = {"size": 100, "score": 0, "id": "Topics", "type": "triangle-up"}
    nodes.append(node)
    words_dict = {}

    # Initializes all topic nodes and connects all topic nodes to the root node
    for r in range(0, num_topics):
        nodes.append({'size': 50, 'score': 0.5, 'id': 'Topic ' + str(r + 1), 'type': 'square'})
        links.append({'source': 0, 'target': r})

    for key, value in topics_dict.items():
        for val in value:
            target = words_dict.get(val['word'])
            if target is None:
                target = len(words_dict) + num_topics + 1
                words_dict[val['word']] = target
                nodes.append({'size': 10, 'score': 1, 'id': val['word'], 'type': 'circle'})

            links.append({'source': int(key), 'target': target})

    # for ind in range(1, (num_topics * no_top_words) + num_topics):
    #
    #     if topic_node is True or ind == 1:
    #         node = {}
    #         link = {}
    #         topic_cnt += 1
    #         node["size"] = 50
    #         node["score"] = 0.5
    #         node["id"] = "Topic" + str(topic_cnt)
    #         node["type"] = "square"
    #         node["value"] = "Topic" + str(topic_cnt)
    #
    #         link["source"] = 0
    #         link["target"] = ind
    #
    #         links.append(link)
    #         nodes.append(node)
    #
    #         destination_num = ind + 1

            # Initializes all word nodes and their corresponding links
    #         if node_cnt < num_topics and dict_count < num_topics:
    #             dict_count += 1
    #             while count < no_top_words:
    #                 node = {}
    #                 link = {}
    #                 # Getting the topic words from the dictionary
    #                 word = list(topics_dict[str(dict_count)])[count]['word']
    #                 # Getting the score of each topic word for each topic from the dictionary
    #                 score = round(list(topics_dict[str(dict_count)])[count]['score'], 2)
    #                 # link["source"] = ind
    #                 link["target"] = destination_num
    #                 links.append(link)
    #                 node["size"] = 10
    #                 node["score"] = score
    #                 node["id"] = str(word)
    #                 node["type"] = "circle"
    #                 nodes.append(node)
    #                 count += 1
    #                 destination_num += 1
    #             count = 0
    #
    #         node_cnt += 1
    #         topic_node = False
    #
    #     # Used to identify if the next index is a topic node. If the current node is divisible by 16 then it means that
    #     # it's the last word node for the current topic. It follows that the next node should be a topic node
    #     # of the next topic
    #     if ind % (no_top_words + 1) == 0:
    #         print("Index" + str(ind))
    #         topic_node = True
    #
    # Adding the nodes and links to the json string
    json_string["links"] = links
    json_string["nodes"] = nodes
    json_string["graphs"] = []

    script_path = os.path.dirname(__file__)
    json_url = os.path.join(script_path, os.path.pardir, "graphs.json")

    with open(json_url, 'w') as tst:
        json.dump(json_string, tst, sort_keys=True)


    # insert JSON file processing
    # save file to graphs.json

    # # used for scatterplot
    # X_topics = lda_model.fit_transform(cvz)
    #
    # # filter out unconfident assignments
    # threshold = 0.5
    # _idx = np.amax(X_topics, axis=1) > threshold  # idx of doc that above the threshold
    # X_topics = X_topics[_idx]
    #
    # # a t-SNE model
    # # angle value close to 1 means sacrificing accuracy for speed
    # # pca initializtion usually leads to better results
    # tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99, init='pca')
    #
    # # 20-D -> 2-D
    # tsne_lda = tsne_model.fit_transform(X_topics)
    #
    # _lda_keys = []
    # for i in range(X_topics.shape[0]):
    #     _lda_keys += X_topics[i].argmax(),
    #
    # # get top words
    # topic_summaries = []
    # topic_word = lda_model.components_  # all topic words
    # vocab = tfidfvec.get_feature_names()
    #
    # for i, topic_dist in enumerate(topic_word):
    #     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(no_top_words + 1):-1]  # get!
    #     topic_summaries.append(' '.join(topic_words))  # append!

    # return topics_dict, X_topics, tsne_lda, lda_model, tfidfvec, no_top_words




    return topics_dict
