from flask import Flask, request, render_template
from controllers.Topic_Analysis.Find_Topic_Tweets import *
from controllers.Topic_Analysis.Topic_Analysis import *


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
    tweets = get_all_tweets()
    topic_for = "All Tweets"
    lda_parameters, tfidf_parameters = topic_analysis()

    print(lda_parameters)
    print(tfidf_parameters)

    tweets_only = [remove_usernames(t['tweet']) for t in tweets]
    final_list = tfidf_vectorizer(tweets_only, tfidf_parameters['min-gram'], tfidf_parameters['max-gram'])
    lda = topic_lda_tfidf(tweets_only, lda_parameters['min-gram'], lda_parameters['max-gram'],
                          lda_parameters['topic'], lda_parameters['iter'], lda_parameters['word'])
    find_topic_tweets(lda, tweets)
    save_obj(final_list, "tf_idf")

    return render_template("analysis/Topic/view_topic_analysis.html", tf_idf=final_list, topics_dict=lda,
                           topic_analysis_for=topic_for)


def view_candidate(candidate_name):
    topic_for = candidate_name

    lda_parameters, tfidf_parameters = topic_analysis()

    tweets = load_obj("Tweets")
    topic_for = "Candidate: " + candidate_name

    tweets_only = [remove_usernames(t['tweet']) for t in tweets]
    final_list = tfidf_vectorizer(tweets_only, tfidf_parameters['min-gram'], tfidf_parameters['max-gram'])
    lda = topic_lda_tfidf(tweets_only, lda_parameters['min-gram'], lda_parameters['max-gram'],
                          lda_parameters['topic'], lda_parameters['iter'], lda_parameters['word'])
    find_topic_tweets(lda, tweets)
    save_obj(final_list, "tf_idf")

    return render_template("analysis/Topic/view_topic_analysis.html", tf_idf=final_list, topics_dict=lda,
                               topic_analysis_for=topic_for)


def view_sentiment(sentiment):
    topic_for = sentiment
    lda_parameters, tfidf_parameters = topic_analysis()

    data = load_obj("Sentiment")
    tweets = data[sentiment]
    topic_for = sentiment + "Sentiment"

    tweets_only = [remove_usernames(t['tweet']) for t in tweets]
    final_list = tfidf_vectorizer(tweets_only, tfidf_parameters['min-gram'], tfidf_parameters['max-gram'])
    lda = topic_lda_tfidf(tweets_only, lda_parameters['min-gram'], lda_parameters['max-gram'],
                          lda_parameters['topic'], lda_parameters['iter'], lda_parameters['word'])
    find_topic_tweets(lda, tweets)
    save_obj(final_list, "tf_idf")

    return render_template("analysis/Topic/view_topic_analysis.html", tf_idf=final_list, topics_dict=lda,
                           topic_analysis_for=topic_for)