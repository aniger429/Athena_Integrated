from controllers.Sentiment_Analysis.Sentiment_Identification import *
from DBModels.Tweet import *
from controllers.Candidate_Analysis.Candidate_Identification import *
from flask import Flask, request, render_template,redirect, url_for


def get_sentiment_identified(tweets):
    positive_tweets, neutral_tweets, negative_tweets = compute_tweets_sentiment(tweets)
    positive_tweets = {'tweets': positive_tweets, 'candidate_mentioned': identify_candidate_mentioned(positive_tweets)}
    neutral_tweets = {'tweets': neutral_tweets, 'candidate_mentioned': identify_candidate_mentioned(neutral_tweets)}
    negative_tweets = {'tweets': negative_tweets, 'candidate_mentioned': identify_candidate_mentioned(negative_tweets)}

    return positive_tweets, neutral_tweets, negative_tweets


# def view_candidate(viz_selected, candidate):
#     # tweets = get_all_tweets()
#     sentiment_for = "Candidate: " + candidate
#
#     positive_tweets, neutral_tweets, negative_tweets = get_sentiment_identified(tweets)
#
#     identify_candidate(tweets, cname=cname)
#     data = load_obj("Candidate")
#     candidate_name_count = Counter([tweet['tweet'][tweet['cand_ana'][cname]] for tweet in data])
#
#     if viz_selected == "Concordancer with Sentiment":
#         return render_template("analysis/Sentiment/view_concordancer_sentiment.html",
#                     tweet_list=[negative_tweets, positive_tweets, neutral_tweets],
#                     sentiment_labels=['negative', 'neutral', 'positive'], sentiment_analysis_for=sentiment_for)
#
#         return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
#                                candidate_data=get_specific_candidate_names(cname),
#                                candidate_tweets=data)


    return render_template("analysis/Sentiment/view_tweets_sentiment.html", tweet_list=[negative_tweets, positive_tweets, neutral_tweets], sentiment_labels=['negative', 'neutral', 'positive'], sentiment_analysis_for=sentiment_for)



def view_sentiment_analysis():
    tweets = get_all_tweets()
    datasource = request.args.get('datasource')
    sentiment_for = "All"

    if datasource == "Topic":
        key = request.args.get('key')
        tweets = load_obj("Topics")[key]['topic_tweets']
        sentiment_for = "Topic # "+key

    elif datasource == "Candidate":
        candidate_name = request.args.get('candidate_name')
        tweets = load_obj("Tweets")
        sentiment_for="Candidate: "+candidate_name

    positive_tweets, neutral_tweets, negative_tweets = compute_tweets_sentiment(tweets)

    positive_tweets = {'tweets': positive_tweets, 'candidate_mentioned': identify_candidate_mentioned(positive_tweets)}
    neutral_tweets = {'tweets': neutral_tweets, 'candidate_mentioned': identify_candidate_mentioned(neutral_tweets)}
    negative_tweets = {'tweets': negative_tweets, 'candidate_mentioned': identify_candidate_mentioned(negative_tweets)}

    return render_template("analysis/Sentiment/view_tweets_sentiment.html", tweet_list=[negative_tweets, positive_tweets, neutral_tweets], sentiment_labels=['negative', 'neutral', 'positive'], sentiment_analysis_for=sentiment_for)
