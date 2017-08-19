from flask import redirect, url_for, session
from controllers.Candidate_Analysis.Candidate_Identification import *
from controllers.Sentiment_Analysis.Sentiment_Identification import *
from controllers.analysis_controller.topic_view_analysis import *


def new_analysis():
    flevel, slevel, tlevel = request.form['steps'].split("-")
    analyzing_for = session.get('analysis_name', 'Candidate')
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
                posi_tweets, neut_tweets, neg_tweets = compute_tweets_sentiment(data)

                final_tweets = posi_tweets.append(neut_tweets)
                final_tweets = final_tweets.append(neg_tweets)
                final_tweets = final_tweets.sample(frac=1).reset_index(drop=True)

                senti_count = {'positive': len(posi_tweets), 'neutral': len(neut_tweets), 'negative': len(neg_tweets)}

                return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                                       candidate_data=get_specific_candidate_names(candidate_name),
                                       candidate_tweets=final_tweets,
                                       withsenti=True, senti_count=senti_count, analyzing_for=analyzing_for)

            if viz_selected == "stacked bar chart":
                final_tweets = compute_tweets_sentiment(data)

                senti_count = Counter(tweet['sentiment'] for tweet in final_tweets if tweet.get('sentiment'))

                return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                                       candidate_data=get_specific_candidate_names(candidate_name), candidate_tweets=final_tweets,
                                       withsenti=True, senti_count=senti_count)

            return redirect(url_for('view_sentiment_analysis', datasource='Candidate', candidate_name=candidate_name, analyzing_for=analyzing_for))
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
