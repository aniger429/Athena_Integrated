from flask import request, redirect, url_for, render_template
from controllers.Candidate_Analysis.Candidate_Identification_Final import *
from collections import Counter
from controllers.analysis_controller.view_analysis import *


def candidate_analysis(tweets, candidate_name):
    identify_candidate(tweets, candidate_name)
    data = load_obj("Candidate")
    candidate_name_count = Counter([tweet['tweet'][tweet['cand_ana'][candidate_name]] for tweet in data])
    return candidate_name_count, data


def new_analysis():
    steps = request.form['steps'].split("-")
    print("again and again")

    # first level
    if steps[0] == "candidate":
        candidate_name = request.form['candidate-name']
        print("flevel: candidate")
        tweets = get_all_tweets()
        candidate_name_count, data = candidate_analysis(tweets, candidate_name)

        if steps[1] == "topic":
            print("slevel: topic")
            return view_candidate(candidate_name)

        elif steps[1] == "sentiment":
            print("slevel: sentiment")
            return redirect(url_for('view_sentiment_analysis', datasource='Candidate', candidate_name=candidate_name))


        return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                               candidate_data=get_specific_candidate_names(candidate_name),
                               candidate_tweets=data)
    # first level
    elif (steps[0] == "topic"):
        print("flvel: topic")
        return view_all()

    # first level
    else:
        print("flevel: sentiment")
        return redirect(url_for('view_sentiment_analysis'))