import re

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


from sklearn.utils import shuffle
from controllers.machine_learning.cleaning import *

def preprocess(file_name, samples):
    data = pd.read_excel(file_name, parse_cols='B,G')
    removeSp = re.compile(r'@(\w+)')

    for i in range(0, len(data[:samples])):
        data['Tweet'][i] = data_cleaning(data['Tweet'][i])
        data['Tweet'][i] = removeSp.sub('', data['Tweet'][i])
    data = shuffle(data)    
    # data = data[:samples]
    
    return data

def train(data, index):
    if (index == 1): # Naive Bayes
        text_clf = Pipeline([('vect',CountVectorizer()),('tfidf',TfidfTransformer()),('clf',MultinomialNB())])
    elif (index == 2): # SVM
        text_clf = Pipeline([('vect',CountVectorizer()),('tfidf',TfidfTransformer()),('clf',SGDClassifier())])
    elif (index == 3): # KNN
        text_clf = Pipeline([('vect',CountVectorizer()),('tfidf',TfidfTransformer()),('clf',KNeighborsClassifier())])
    elif (index == 4): # Decision Tree
        text_clf = Pipeline([('vect',CountVectorizer()),('tfidf',TfidfTransformer()),('clf',DecisionTreeClassifier())])
    elif (index == 5): # Maximum Entropy
        text_clf = Pipeline([('vect',CountVectorizer()),('tfidf',TfidfTransformer()),('clf',LogisticRegression())])
    text_clf = text_clf.fit(data['Tweet'],data['Sentiment'])
    
    return text_clf


def decideSentiment(tweet ,df, text_clf):
    data = shuffle(df)
    data = data[:1]
    data[:1].Tweet = tweet
    docs_test = data.Tweet
    predict = text_clf.predict(docs_test)
    #print(np.mean(predict == data.Sentiment))
    print(data.Tweet)
    print(predict)

data = preprocess('../../Data/Election-18.xlsx', 100)

nb = train(data, 1)
svm  = train(data, 2)
knn = train(data, 3)
dt = train(data, 4)
me = train(data, 5)

decideSentiment('Anong gagawin natin?! Puro kayo reklamo putangina nyo #DUTERTE https://t.co/pibO3KGeWH', data, nb)
decideSentiment('I hate bananas but i love strawberries', data, nb)
decideSentiment('I love bananas', data, nb)



