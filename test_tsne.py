import numpy as np
from bokeh.charts import show
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource, figure
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE

from DBModels.Tweet import *


def lda():
    tweets = [t['tweet'] for t in get_tweets_only()[:1000]]

    n_topics = 12  # number of topics
    n_iter = 500  # number of iterations

    # vectorizer: ignore English stopwords & words that occur less than 5 times
    cvectorizer = CountVectorizer(min_df=5, stop_words='english')
    cvz = cvectorizer.fit_transform(tweets)

    # train an LDA model
    lda_model = LatentDirichletAllocation(n_topics=n_topics, max_iter=n_iter,
                                          learning_method='batch')
    X_topics = lda_model.fit_transform(cvz)

    # filter out unconfident assignments
    threshold = 0.5
    _idx = np.amax(X_topics, axis=1) > threshold  # idx of doc that above the threshold
    X_topics = X_topics[_idx]

    # a t-SNE model
    # angle value close to 1 means sacrificing accuracy for speed
    # pca initializtion usually leads to better results
    tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99, init='pca')

    # 20-D -> 2-D
    tsne_lda = tsne_model.fit_transform(X_topics)

    n_top_words = 5   # number of keywords we show

    # 20 colors
    colormap = np.array([
      "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
      "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
      "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
      "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"
    ])

    _lda_keys = []
    for i in range(X_topics.shape[0]):
        _lda_keys += X_topics[i].argmax(),

    # get top words
    topic_summaries = []
    topic_word = lda_model.components_  # all topic words
    vocab = cvectorizer.get_feature_names()

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]  # get!
        topic_summaries.append(' '.join(topic_words))  # append!

    #  plot
    title = 'Tweets LDA viz'
    num_example = len(X_topics)

    plot_lda = figure(plot_width=1000, plot_height=500,
                      title=title,
                      tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
                      x_axis_type=None, y_axis_type=None, min_border=1)

    source = ColumnDataSource({'content': tweets[:num_example], 'topic_key': _lda_keys[:num_example],
                               'x': tsne_lda[:, 0], 'y': tsne_lda[:, 1],
                               'color': colormap[_lda_keys][:num_example]})

    plot_lda.scatter(x='x', y='y', color='color', source=source)

    # randomly choose a news (within a topic) coordinate as the crucial words coordinate
    topic_coord = np.empty((X_topics.shape[1], 2)) * np.nan
    for topic_num in _lda_keys:
        if not np.isnan(topic_coord).any():
            break
        topic_coord[topic_num] = tsne_lda[_lda_keys.index(topic_num)]

    # plot crucial words
    for i in range(X_topics.shape[1]):
        plot_lda.text(topic_coord[i, 0], topic_coord[i, 1], [topic_summaries[i]])

    # hover tools
    hover = plot_lda.select(dict(type=HoverTool))
    hover.tooltips = {"content": "@content - topic: @topic_key"}

    print("done")

    # output_file("donut.html", title="donut.py example")
    show(plot_lda)

lda()
