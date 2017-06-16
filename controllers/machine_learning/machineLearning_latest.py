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
    data = data[:samples]
    
    return data


def train(dataX, dataY, index):
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
    text_clf = text_clf.fit(dataX,dataY)
    
    return text_clf

def accuracy(data):
    # load dataset
    seed = 7
    X = data['Tweet']
    Y = data['Sentiment']
    #test/validation size
    size = 0.5
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=size, random_state=seed)
    print(X_train.shape)
    print(Y_train.shape)
    print(X_validation.shape)
    print(Y_validation.shape)


    # prepare models
    models = []
    #models.append(('LR', LogisticRegression()))
    #models.append(('LDA', LinearDiscriminantAnalysis()))
    #models.append(('KNN', KNeighborsClassifier()))
    #models.append(('CART', DecisionTreeClassifier()))
    #models.append(('NB', GaussianNB()))
    #models.append(('SVM', SVC()))
    models.append(('NB', train(data['Tweet'], data['Sentiment'],1)))
    models.append(('LR', train(data['Tweet'], data['Sentiment'],5)))
    models.append(('SVM', train(data['Tweet'], data['Sentiment'],2)))
    models.append(('KNN', train(data['Tweet'], data['Sentiment'],3)))
    models.append(('CART', train(data['Tweet'], data['Sentiment'],4)))
    
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
        print(kfold)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold)
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

    # test
    decideSentiment('I love bananas', X_validation, train(X_train, Y_train, 1))
    decideSentiment('I love bananas', X_validation, train(X_train, Y_train, 2))
    decideSentiment('I love bananas', X_validation, train(X_train, Y_train, 3))
    decideSentiment('I love bananas', X_validation, train(X_train, Y_train, 4))
    decideSentiment('I love bananas', X_validation, train(X_train, Y_train, 5))
    


def decideSentiment(tweet ,df, text_clf):
    a = []
    a.append(tweet)
    predict = text_clf.predict(a)
    #print(np.mean(predict == data.Sentiment))
    print(tweet)
    print(predict)


data = preprocess('../../Data/Election-18.xlsx', 2000)
accuracy(data)

#nb = train(data, 1)
#svm  = train(data, 2)
#knn = train(data, 3)
#dt = train(data, 4)
#me = train(data, 5)
#decideSentiment('Anong gagawin natin?! Puro kayo reklamo putangina nyo #DUTERTE https://t.co/pibO3KGeWH', data, nb)
#decideSentiment('I hate bananas but i love strawberries', data, nb)
#decideSentiment('I love bananas', data, nb)


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


#test('../../Data/Election-18.xlsx')
