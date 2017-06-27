from bokeh.charts import Donut, show, output_file
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data

import pandas as pd


def load_chart():
    # utilize utility to make it easy to get json/dict data converted to a dataframe
    df = df_from_json(data)

    # filter by countries with at least one medal and sort by total medals
    df = df[df['total'] > 8]
    df = df.sort_values("total", ascending=False)
    df = pd.melt(df, id_vars=['abbr'],
                 value_vars=['bronze', 'silver', 'gold'],
                 value_name='medal_count', var_name='medal')

    # original example
    d = Donut(df, label=['abbr', 'medal'], values='medal_count',
              text_font_size='12pt', hover_text='medal_count', plot_height=800, plot_width=800)

    return d