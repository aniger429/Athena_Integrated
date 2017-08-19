from flask import request, render_template, session

from controllers.Topic_Analysis.Find_Topic_Tweets import *
from controllers.Topic_Analysis.Topic_Analysis import *
from controllers.visualization.wordcloud_viz import word_cloud
from DBModels.Tweet import *
import base64

def topic_analysis():
    # get parameters from the form submitted
    # lda parameters

    lda_parameters = {}
    lda_parameters['min-gram'] = int(request.form['lda-min-gram'])
    lda_parameters['max-gram'] = int(request.form['lda-max-gram'])
    lda_parameters['iter'] = int(request.form['lda-iter'])
    lda_parameters['word'] = int(request.form['lda-word'])
    lda_parameters['topic'] = int(request.form['lda-topic'])

    # tfidf parameters
    tfidf_parameters = {}
    tfidf_parameters['min-gram'] = int(request.form['tfidf-min-gram'])
    tfidf_parameters['max-gram'] = int(request.form['tfidf-max-gram'])

    return lda_parameters, tfidf_parameters


def view_all():
    tweets = get_all_orig_tweets()
    topic_for = "All Tweets"
    lda_parameters, tfidf_parameters = topic_analysis()

    tweets_only = list(tweets['tweet'])
    final_list = tfidf_vectorizer(tweets_only, tfidf_parameters['min-gram'], tfidf_parameters['max-gram'])

    topics_dict = topic_analysis_lda(tweets_only,
                                     lda_parameters['min-gram'],
                                     lda_parameters['max-gram'],
                                     lda_parameters['topic'],
                                     lda_parameters['iter'],
                                     lda_parameters['word'])

    word_cloud_path = word_cloud("all", final_list)
    wc_img = base64.b64encode(open(word_cloud_path, "rb").read())

    # script, div = scatter_plot(tweets_only, X_topics, tsne_lda, lda_model, tfidfvec, no_top_words)

    find_topic_tweets(topics_dict, tweets)
    save_obj(final_list, "tf_idf")

    return render_template("analysis/Topic/view_topic_results.html",
                           tf_idf=final_list, topics_dict=topics_dict,
                           topic_analysis_for=topic_for, source="All Tweets", wc_img=wc_img.decode('utf8'))


def view_candidate(candidate_name):
    lda_parameters, tfidf_parameters = topic_analysis()

    tweets = load_pickled_dataframe("Candidate")
    topic_for = session.get('analysis_name', 'Candidate')
    tweets_only = list(tweets['tweet'])
    final_list = tfidf_vectorizer(tweets_only, tfidf_parameters['min-gram'], tfidf_parameters['max-gram'])

    topics_dict = topic_analysis_lda(tweets_only,
                                     lda_parameters['min-gram'],
                                     lda_parameters['max-gram'],
                                     lda_parameters['topic'],
                                     lda_parameters['iter'],
                                     lda_parameters['word'])

    word_cloud_path = word_cloud("candidate", final_list)
    wc_img = base64.b64encode(open(word_cloud_path, "rb").read())

    find_topic_tweets(topics_dict, tweets)
    save_obj(final_list, "tf_idf")

    return render_template("analysis/Topic/view_topic_results.html", tf_idf=final_list, topics_dict=topics_dict,
                           topic_analysis_for=topic_for, source=candidate_name, wc_img=wc_img.decode('utf8'))


def view_sentiment(sentiment):
    topic_for = sentiment
    lda_parameters, tfidf_parameters = topic_analysis()

    tweets = load_pickled_dataframe(sentiment)
    topic_for = sentiment

    tweets_only = list(tweets['tweet'])
    final_list = tfidf_vectorizer(tweets_only, tfidf_parameters['min-gram'], tfidf_parameters['max-gram'])

    topics_dict = topic_analysis_lda(tweets_only,
                                     lda_parameters['min-gram'],
                                     lda_parameters['max-gram'],
                                     lda_parameters['topic'],
                                     lda_parameters['iter'],
                                     lda_parameters['word'])

    word_cloud_path = word_cloud(sentiment, final_list)
    wc_img = base64.b64encode(open(word_cloud_path, "rb").read())

    find_topic_tweets(topics_dict, tweets)
    save_obj(final_list, "tf_idf")

    return render_template("analysis/Topic/view_topic_results.html", tf_idf=final_list, topics_dict=topics_dict,
                           topic_analysis_for=topic_for, source=sentiment, wc_img=wc_img.decode('utf8'))
