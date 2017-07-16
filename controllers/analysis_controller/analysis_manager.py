from flask import redirect, url_for
from controllers.Candidate_Analysis.Candidate_Identification import *
from controllers.analysis_controller.topic_view_analysis import *
from controllers.Sentiment_Analysis.Sentiment_Identification import *


def candidate_analysis(tweets, candidate_name):
    #  do candidate analysis on the tweets
    identify_candidate(tweets, candidate_name)
    # load cand
    data = load_pickled_dataframe("Candidate")

    data['name'] = data.apply(lambda row: (row['orig_tweets'][row[candidate_name]]), axis=1)

    candidate_name_count = Counter(list(data['name']))

    return candidate_name_count, data


def new_analysis():
    flevel, slevel, tlevel = request.form['steps'].split("-")
    print("here" + flevel)
    
    # first level
    if flevel == "candidate":
        print("flevel: candidate")
        candidate_name = request.form['candidate-name']
        tweets = get_all_orig_tweets()
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

                return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                                       candidate_data=get_specific_candidate_names(candidate_name), candidate_tweets=final_tweets,
                                       withsenti=True, senti_count=senti_count)

            if viz_selected == "stacked bar chart":
                final_tweets = compute_senti_candidate_tweet(data)

                senti_count = Counter(tweet['sentiment'] for tweet in final_tweets if tweet.get('sentiment'))

                return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                                       candidate_data=get_specific_candidate_names(candidate_name), candidate_tweets=final_tweets,
                                       withsenti=True, senti_count=senti_count)

            return redirect(url_for('view_sentiment_analysis', datasource='Candidate', candidate_name=candidate_name))
        return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                               candidate_data=get_specific_candidate_names(candidate_name), candidate_tweets=data, withsenti=False)
    # first level
    elif flevel == "topic":
        print("flvel: topic")

        return view_all()

    # first level
    else:
        print("flevel: sentiment")
        return redirect(url_for('view_sentiment_analysis'))
