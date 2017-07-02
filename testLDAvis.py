import pyLDAvis
from controllers.Topic_Analysis.Topic_Analysis import *
from controllers.Topic_Analysis.pyldavis_to_sklearn import *
from DBModels.Tweet import *


tweets = [t['tweet'] for t in get_tweets_only()[:100]]

# movies_model_data = topic_lda_tfidf(tweets, 1, 3, 10, 1000, no_top_words=15)
lda_tf, dtm_tf, tf_vectorizer = testing(tweets)

vis = prepare(lda_tf, dtm_tf, tf_vectorizer)
pyLDAvis.show(vis)
# movies_vis_data = pyLDAvis.prepare(**movies_model_data)
# pyLDAvis.display(movies_vis_data)