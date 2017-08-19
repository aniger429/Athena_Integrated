import pyLDAvis

from DBModels.Tweet import *
from controllers.Topic_Analysis.pyldavis_to_sklearn import *

tweets = [t['tweet'] for t in get_tweets_only()[:1000]]

# movies_model_data = topic_lda_tfidf(tweets, 1, 3, 10, 1000, no_top_words=15)
lda_tf, dtm_tf, tf_vectorizer = testing(tweets)

vis = prepare(lda_tf, dtm_tf, tf_vectorizer)
pyLDAvis.save_html(vis, "/home/dudegrim/Documents/banana.html")

# movies_vis_data = pyLDAvis.prepare(**movies_model_data)
# pyLDAvis.display(movies_vis_data)



