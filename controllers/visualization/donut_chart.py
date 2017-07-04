from bokeh.charts import Donut, show, output_file
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data

import pandas as pd

from bokeh.charts import Bar, output_file, show
from bokeh.sampledata.autompg import autompg as df
from controllers.Candidate_Analysis.Candidate_Identification import *
from bokeh.embed import components

def load_chart():
    # # utilize utility to make it easy to get json/dict data converted to a dataframe
    # df = df_from_json(data)
    #
    #
    # # filter by countries with at least one medal and sort by total medals
    # df = df[df['total'] > 8]
    # df = df.sort_values("total", ascending=False)
    # print(df)
    # df = pd.melt(df, id_vars=['abbr'],
    #              value_vars=['bronze', 'silver', 'gold'],
    #              value_name='medal_count', var_name='medal')
    #
    # # original example
    # d = Donut(df, label=['abbr', 'medal'], values='medal_count',
    #           text_font_size='12pt', hover_text='medal_count', plot_height=800, plot_width=800)




    plot = Bar(df, label='origin', values='mpg', agg='mean', stack='cyl',
            title="Avg MPG by ORIGIN, stacked by CYL", legend='top_right')

    # Embed plot into HTML via Flask Render
    script, div = components(plot)

    return script, div

def tweet_sentiment_per_candidate():
    # get all tweets
    tweets = get_all_tweets()
    # candidate analysis all tweets
    identify_candidate()

