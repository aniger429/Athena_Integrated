from flask import request, render_template

from controllers.Candidate_Analysis.Candidate_Identification import *


def get_sentiment_identified(tweets):
    positive_tweets, neutral_tweets, negative_tweets = compute_tweets_sentiment(tweets)
    positive_tweets = {'tweets': positive_tweets, 'candidate_mentioned': identify_candidate_mentioned(positive_tweets)}
    neutral_tweets = {'tweets': neutral_tweets, 'candidate_mentioned': identify_candidate_mentioned(neutral_tweets)}
    negative_tweets = {'tweets': negative_tweets, 'candidate_mentioned': identify_candidate_mentioned(negative_tweets)}

    return positive_tweets, neutral_tweets, negative_tweets


def view_sentiment_analysis():
    tweets = get_all_tweets()
    datasource = request.args.get('datasource')
    sentiment_for = "All"

    if datasource == "Topic":
        key = request.args.get('key')
        tweets = load_obj("Topics")[key]['topic_tweets']
        sentiment_for = "Topic # " + key

    elif datasource == "Candidate":
        candidate_name = request.args.get('candidate_name')
        tweets = load_obj("Tweets")
        sentiment_for = "Candidate: " + candidate_name

    positive_tweets, neutral_tweets, negative_tweets = compute_tweets_sentiment(tweets)

    positive_tweets = {'tweets': positive_tweets, 'candidate_mentioned': identify_candidate_mentioned(positive_tweets)}
    neutral_tweets = {'tweets': neutral_tweets, 'candidate_mentioned': identify_candidate_mentioned(neutral_tweets)}
    negative_tweets = {'tweets': negative_tweets, 'candidate_mentioned': identify_candidate_mentioned(negative_tweets)}

    return render_template("analysis/Sentiment/view_tweets_sentiment.html",
                           tweet_list=[negative_tweets, positive_tweets, neutral_tweets],
                           sentiment_labels=['negative', 'neutral', 'positive'], sentiment_analysis_for=sentiment_for)
