import cleaning as cl
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
import re
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression


data = pd.read_excel('Election-18.xlsx', parse_cols='B,G')
removeSp = re.compile(r'@(\w+)')

for i in range(0, len(data)):
    data['Tweet'][i] = cl.dataCleaning(data['Tweet'][i])
    data['Tweet'][i] = removeSp.sub('', data['Tweet'][i])
data = shuffle(data)    
data = data[:3500]
text_clf = Pipeline([('vect',CountVectorizer()),('tfidf',TfidfTransformer()),('clf',LogisticRegression())])
text_clf = text_clf.fit(data['Tweet'],data['Sentiment'])


data = shuffle(data)
data = data[:1500]

docs_test = data.Tweet

predict = text_clf.predict(docs_test)
print(np.mean(predict == data.Sentiment))
