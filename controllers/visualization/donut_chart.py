from bokeh.charts import Donut, show, output_file
from controllers.Candidate_Analysis.Candidate_Identification import *
from bokeh.embed import components


def donut_chart(data_series):
    pie_chart = Donut(data_series, plot_height=700, plot_width=800)

    # Embed plot into HTML via Flask Render
    script, div = components(pie_chart)

    return script, div


def tweet_sentiment_per_candidate():
    # get all tweets
    tweets = get_all_tweets()
    # candidate analysis all tweets
    identify_candidate()

