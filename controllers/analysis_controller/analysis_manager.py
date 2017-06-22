from flask import request, redirect, url_for, render_template
from controllers.Candidate_Analysis.Candidate_Identification import *
from controllers.Topic_Analysis.Topic_Analysis import *
from collections import Counter
from controllers.Topic_Analysis.Find_Topic_Tweets import *
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
            # data = load_obj('Tweets')
            # final_list, lda = topic_analysis(tweets)
            return redirect(url_for('view_topic_analysis', datasource='candidate', candidate_name=candidate_name))
            # return render_template("analysis/Topic/view_topic_analysis.html", tf_idf=final_list, topics_dict=lda, topic_analysis_for=candidate_name)

        elif slevel == "sentiment":
            print("slevel: sentiment")
            viz_selected = request.form['viz_selected']

            if viz_selected == "Concordancer with Sentiment":
                final_tweets= compute_senti_candidate_tweet(data)
                return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                                       candidate_data=get_specific_candidate_names(candidate_name), candidate_tweets=final_tweets, withsenti=True)

            return redirect(url_for('view_sentiment_analysis', datasource='Candidate', candidate_name=candidate_name))


        return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                               candidate_data=get_specific_candidate_names(candidate_name), candidate_tweets=data, withsenti=False)
    # first level
    elif (flevel == "topic"):
        print("flvel: topic")
        # topic_tweets = list(get_all_tweets())
        # final_list, lda = topic_analysis(topic_tweets)

        # if slevel == "none":
        #     print("slevel: none")
        # elif slevel == "candidate":
        #     print("slevel: candidate")
        #
        #     if tlevel == "none":
        #         print("tlevel: none")
        #     elif tlevel == "sentiment":
        #         print("tlevel: sentiment")
        # else:
        #     print("slevel: sentiment")
        #     if tlevel == "none":
        #         print("tlevel: none")
        #     elif tlevel == "candidate":
        #         print("tlevel: candidate")

        return redirect(url_for('view_topic_analysis'))
    # first level
    else:
        print("flevel: sentiment")

        # if slevel == "none":
        #     print("slevel: none")
        # elif slevel == "candidate":
        #     print("slevel: candidate")
        #
        #     if tlevel == "none":
        #         print("tlevel: none")
        #     elif tlevel == "topic":
        #         print("tlevel: topic")
        # else:
        #     print("slevel: topic")
        #     if tlevel == "none":
        #         print("tlevel: none")
        #     elif tlevel == "candidate":
        #         print("tlevel: candidate")


        return redirect(url_for('view_sentiment_analysis'))