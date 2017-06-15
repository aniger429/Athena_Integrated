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

def accuracy(file_name):
    # load dataset
    names = ['tweet', 'sentiment']
    dataframe = pd.read_excel(file_name, parse_cols='B,G')[:500]

    array = dataframe.values
    X = array[:, 0:1]
    Y = array[:, 1]





    # prepare configuration for cross validation test harness
    seed = 7
    # prepare models
    models = []
    models.append(('LR', LogisticRegression()))
    models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC()))
    # evaluate each model in turn
    results = []
    names = []
    scoring = 'accuracy'

    # evaluate each model in turn
    results = []
    names = []
    scoring = 'accuracy'
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
    # boxplot algorithm comparison
    fig = plt.figure()
    fig.suptitle('Algorithm Comparison')
    ax = fig.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names)
    plt.show()


def decideSentiment(tweet ,df, text_clf):
    data = shuffle(df)
    data = data[:1]
    data[:1].Tweet = tweet
    docs_test = data.Tweet
    predict = text_clf.predict(docs_test)
    #print(np.mean(predict == data.Sentiment))
    print(data.Tweet)
    print(predict)

# data = preprocess('../../Data/Election-18.xlsx', 100)
#
# nb = train(data, 1)
# # svm  = train(data, 2)
# # knn = train(data, 3)
# # dt = train(data, 4)
# # me = train(data, 5)
#
# decideSentiment('Anong gagawin natin?! Puro kayo reklamo putangina nyo #DUTERTE https://t.co/pibO3KGeWH', data, nb)
# decideSentiment('I hate bananas but i love strawberries', data, nb)
# decideSentiment('I love bananas', data, nb)

# accuracy('../../Data/Election-18.xlsx')

def test(file_name):
    # load dataset
    train_data = pd.read_excel(file_name, parse_cols='B,G')[:500]
    tweet = [data_cleaning(tweet) for tweet in train_data["Tweet"]]

    vectorizer = TfidfVectorizer(min_df=1,
                                 max_df=0.8,
                                 sublinear_tf=True,
                                 use_idf=True)

    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.fit(train_data)


test('../../Data/Election-18.xlsx')