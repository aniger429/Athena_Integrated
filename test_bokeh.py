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

from bokeh.charts import Donut, show
import pandas as pd
data = pd.Series([100, 500, 200], index=['Positive', 'Negative', 'Neutral'])
pie_chart = Donut(data)
show(pie_chart)