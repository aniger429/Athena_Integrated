# from bokeh.charts import Donut, show, output_file
# from bokeh.charts.utils import df_from_json
# from bokeh.sampledata.olympics2014 import data
#
# import pandas as pd
#
# # utilize utility to make it easy to get json/dict data converted to a dataframe
# df = df_from_json(data)
#
# # filter by countries with at least one medal and sort by total medals
# df = df[df['total'] > 8]
# df = df.sort_values("total", ascending=False)
# df = pd.melt(df, id_vars=['abbr'],
#              value_vars=['bronze', 'silver', 'gold'],
#              value_name='medal_count', var_name='medal')
#
# # original example
# d = Donut(df, label=['abbr', 'medal'], values='medal_count',
#           text_font_size='8pt', hover_text='medal_count')
#
# output_file("donut.html", title="donut.py example")
#
# show(d)

from bokeh.models import Label
from bokeh.plotting import figure
from bokeh.plotting import show

words = [
    ('hello', (10, 100), '12pt', 0.8),
    ('how', (20, 10), '14pt', 0.8),
    ('are', (100, 20), '16pt', 0.8),
    ('you', (50, 30), '18pt', 0.8),
    ('???', (100, 100), '18pt', 0.8),
]

fig = figure(plot_width=200, plot_height=200, title='test')

for word, loc, size, alpha in words:
    w = Label(x=loc[0], y=loc[1], x_units='screen', y_units='screen',
              text=word, render_mode='css', text_alpha=alpha, text_font_size=size)
    fig.add_layout(w)

show(fig)