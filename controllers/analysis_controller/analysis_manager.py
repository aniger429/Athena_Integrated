from flask import request, redirect, url_for, render_template
from controllers.Candidate_Analysis.Candidate_Identification import *
# from controllers.Topic_Analysis.Topic_Analysis import *
from controllers.analysis_controller.topic_view_analysis import *
from controllers.Sentiment_Analysis.Sentiment_Identification import *


def candidate_analysis(tweets, candidate_name):
    identify_candidate(tweets, candidate_name)
    data = load_obj("Candidate")
    candidate_name_count = Counter([tweet['tweet'][tweet['cand_ana'][candidate_name]] for tweet in data])
    return candidate_name_count, data


def new_analysis():
    print("here")
    flevel,slevel,tlevel = request.form['steps'].split("-")
    candidate_name = request.form['candidate-name']

    # first level
    if flevel == "candidate":
        print("flevel: candidate")
        tweets = get_all_tweets()
        candidate_name_count, data = candidate_analysis(tweets, candidate_name)

        if slevel == "topic":
            print("slevel: topic")
            return view_candidate(candidate_name)

        elif slevel == "sentiment":
            print("slevel: sentiment")
            viz_selected = request.form['viz_selected']

            if viz_selected == "Concordancer with Sentiment":
                final_tweets = compute_senti_candidate_tweet(data)

                senti_count = Counter(tweet['sentiment'] for tweet in final_tweets if tweet.get('sentiment'))
                # print(signs)
                # for sign, count in signs.most_common():
                #     print(sign, count)

                return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                                       candidate_data=get_specific_candidate_names(candidate_name), candidate_tweets=final_tweets,
                                       withsenti=True, senti_count=senti_count)

            return redirect(url_for('view_sentiment_analysis', datasource='Candidate', candidate_name=candidate_name))


        return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                               candidate_data=get_specific_candidate_names(candidate_name), candidate_tweets=data, withsenti=False)
    # first level
    elif (flevel == "topic"):
        print("flvel: topic")
        return view_all()
    # first level
    else:
        print("flevel: sentiment")
        return redirect(url_for('view_sentiment_analysis'))
