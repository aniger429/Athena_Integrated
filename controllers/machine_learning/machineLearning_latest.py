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
from controllers.analysis_controller import Pickle_Saver as ps

# save path for classifiers 
path = 'C:/Users/HKJ/Documents/GitHub/Athena_Integrated/controllers/analysis_controller/Pickles/'

def preprocess(file_name, samples):
    data = pd.read_excel(file_name, parse_cols='B,G')
    removeSp = re.compile(r'@(\w+)')

    for i in range(0, len(data[:samples])):
        data['Tweet'][i] = cl.data_cleaning(data['Tweet'][i])
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

def process(data):
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
    models.append(('NB', train(data['Tweet'], data['Sentiment'],1)))
    models.append(('SVM', train(data['Tweet'], data['Sentiment'],2)))
    models.append(('KNN', train(data['Tweet'], data['Sentiment'],3)))
    models.append(('DT', train(data['Tweet'], data['Sentiment'],4)))
    models.append(('SVM', train(data['Tweet'], data['Sentiment'],5)))
    
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

    #train classifiers
    NB = train(X_train, Y_train, 1)
    SVM = train(X_train, Y_train, 2)
    KNN = train(X_train, Y_train, 3)
    DT = train(X_train, Y_train, 4)
    ME = train(X_train, Y_train, 5)
    
    # test
    decideSentiment('I love bananas', X_validation, NB)
    decideSentiment('I love bananas', X_validation, SVM)
    decideSentiment('I love bananas', X_validation, KNN)
    decideSentiment('I love bananas', X_validation, DT)
    decideSentiment('I love bananas', X_validation, ME)

    # save trained classifiers
    ps.write_pickle(path + 'NB', NB)
    ps.write_pickle(path + 'SVM', SVM)
    ps.write_pickle(path + 'KNN', KNN)
    ps.write_pickle(path + 'DT', DT)
    ps.write_pickle(path + 'ME', ME)

def decideSentiment(tweet ,df, text_clf):
    a = []
    a.append(tweet)
    predict = text_clf.predict(a)
    #print(np.mean(predict == data.Sentiment))
    print(tweet)
    print(predict)


data = preprocess('Election-18.xlsx', 2000)
process(data)
