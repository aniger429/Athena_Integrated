from flask import request, redirect, url_for, render_template
from controllers.Candidate_Analysis.Candidate_Identification_Final import *
from controllers.Topic_Analysis.Topic_Analysis import *
from controllers.Sentiment_Analysis.Sentiment_Identification import *
from collections import Counter
from controllers.Topic_Analysis.Find_Topic_Tweets import *


def candidate_analysis(tweets, candidate_name):
    identify_candidate(tweets, candidate_name)
    data = load_obj("Candidate")
    candidate_name_count = Counter([tweet['tweet'][tweet['cand_ana'][candidate_name]] for tweet in data])
    return candidate_name_count, data


def topic_analysis(tweets):
    tweets_only = [remove_usernames(t['tweet']) for t in tweets]

    final_list = tfidf_vectorizer(tweets_only,1,3)
    lda = topic_lda_tfidf(tweets_only, 1, 1, 10, 100)

    find_topic_tweets(lda, tweets)
    return final_list, lda


def sentiment_analysis(tweets):
    return compute_tweets_sentiment(tweets)


def new_analysis():
    flevel = request.form['first-level']
    slevel = request.form['second-level']
    tlevel = request.form['third-level']
    candidate_name = request.form['candidate-name']

    # first level
    if flevel == "candidate":
        print("flevel: candidate")
        tweets = get_all_tweets()
        candidate_name_count, data = candidate_analysis(tweets, candidate_name)

        if slevel == "topic":
            print("slevel: topic")
            data = load_obj('Tweets')
            final_list, lda = topic_analysis(tweets)

            return render_template("analysis/Topic/view_topic_analysis.html", tf_idf=final_list, topics_dict=lda, topic_analysis_for=candidate_name)

        elif slevel == "sentiment":
            print("slevel: sentiment")
            tweets = load_obj('Tweets')
            print(tweets)
            # tweets = [{'tweet': d['tweet'], '_id':d['_id']} for d in data]
            positive_tweets, neutral_tweets, negative_tweets = sentiment_analysis(tweets)

            return render_template("analysis/view_tweets_sentiment.html",
                                   tweet_list=[negative_tweets, positive_tweets, neutral_tweets],
                                   sentiment_labels=['negative', 'neutral', 'positive'], sentiment_analysis_for=candidate_name)

        return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                               candidate_data=get_specific_candidate_names(candidate_name),
                               candidate_tweets=data)
    # first level
    elif (flevel == "topic"):
        print("flvel: topic")
        topic_tweets = list(get_all_tweets())
        final_list, lda = topic_analysis(topic_tweets)

        if slevel == "none":
            print("slevel: none")
        elif slevel == "candidate":
            print("slevel: candidate")

            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "sentiment":
                print("tlevel: sentiment")
        else:
            print("slevel: sentiment")
            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "candidate":
                print("tlevel: candidate")

        return render_template("analysis/Topic/view_topic_analysis.html", tf_idf=final_list, topics_dict=lda, topic_analysis_for="ALL")
    # first level
    else:
        print("flevel: sentiment")

        if slevel == "none":
            print("slevel: none")
        elif slevel == "candidate":
            print("slevel: candidate")

            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "topic":
                print("tlevel: topic")
        else:
            print("slevel: topic")
            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "candidate":
                print("tlevel: candidate")