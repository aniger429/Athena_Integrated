from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier, PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn import model_selection
from sklearn.metrics import classification_report, confusion_matrix,accuracy_score
from controllers.machine_learning.cleaning import *
from controllers.Pickles.Pickle_Saver import *
from sklearn.externals import joblib
import time

import matplotlib.pyplot as plt
import itertools
import numpy as np


def read_file(file_name):
    # data = pd.read_excel(file_name, parse_cols='B,G')
    data_reader = pd.read_csv(file_name, encoding="utf8", keep_default_na=False, sep=",",
                              skipinitialspace=True, chunksize=25000, usecols=['Tweet', 'Sentiment'],
                              nrows=250000)
    dataset = pd.DataFrame(columns=['Tweet', 'Sentiment'])

    for chunk in data_reader:
        # this processes the tweets
        dataset = dataset.append(clean_tweets_multiprocess(chunk), ignore_index=True)

    dataset = dataset[dataset.Tweet != '']
    dataset = dataset[dataset.Sentiment != ''].head(n=200000)

    return dataset


def train(dataX, dataY, classifier):

    tfidf_vect = TfidfVectorizer(min_df=5, max_df=0.95, use_idf=True, ngram_range=(1, 3))

    if classifier == "NB":  # Naive Bayes
        print("NB")
        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', MultinomialNB())])
    elif classifier == "SVM":  # SVM
        print("SVM")
        text_clf = Pipeline([
                             ('vect', tfidf_vect),
                             ('clf', SGDClassifier(n_jobs=6, warm_start=True))
                           ])
    elif classifier == "KNN":  # KNN
        print("KNN")
        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', KNeighborsClassifier(n_neighbors=7, weights='distance', leaf_size=1000,
                                                          algorithm='ball_tree'))])
    elif classifier == "DT":  # Decision Tree
        print("DT")
        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', DecisionTreeClassifier(max_features='auto', max_depth=100,
                                                            min_samples_leaf=0.0005))])
    elif classifier == "PAC":
        print("PAC")
        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', PassiveAggressiveClassifier(class_weight='balanced', n_jobs=6, warm_start=True))])
    elif classifier == "LSVC":
        print("LSVC")
        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', LinearSVC(class_weight='balanced'))])
    else:  # Maximum Entropy
        print("ME")
        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', LogisticRegression(solver='sag', warm_start=True))])

    text_clf = text_clf.fit(dataX, dataY)
    
    return text_clf


def save_tclf(tclf, index):
    # save path for classifiers
    s_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(s_path, "Pickles", "ML_Classifier")
    pickle.dump(tclf, open(os.path.join(path, index+'.pkl'), 'wb'))


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = np.round(cm.astype('float'), 2) / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, '{:.2f}'.format(cm[i, j]),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    plt.savefig('/home/dudegrim/Documents/Testing/SA/'+title+'.png', bbox_inches='tight')


def process(data, index):
    # load dataset
    seed = 7
    feature = data['Tweet']
    label = data['Sentiment']
    # test/validation size
    size = 0.1
    x_train, x_test, y_train, y_test = model_selection.train_test_split(feature, label,
                                                                        test_size=size, random_state=seed)

    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)

    # train classifiers
    tclf = train(x_train, y_train, index)

    tclf_pred = tclf.predict(x_test)  # produce predictions

    accuracy = accuracy_score(y_test, tclf_pred)
    print("accuracy")
    print(accuracy)
    report = classification_report(y_test, tclf_pred)  # predictions versus actual ones. this will be printed out as a report.

    print(report)
    print("confusion matrix")
    # Compute confusion matrix
    cnf_matrix = confusion_matrix(y_test, tclf_pred, labels=["Positive", "Neutral", "Negative"])
    np.set_printoptions(precision=2)

    print(cnf_matrix)

    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=["Positive", "Neutral", "Negative"], normalize=True,
                          title=index + ' Normalized confusion matrix')

    # save trained classifiers
    save_tclf(tclf, index)


def decideSentiment(tweet, text_clf):  # use this function for sentiment
    a = list()
    a.append(tweet)
    predict = text_clf.predict(a)
    # print(np.mean(predict == data.Sentiment))
    print(tweet)
    print(predict)
    return predict


def main(classifier):
    print(classifier)

    df1 = pd.read_csv('/home/dudegrim/Documents/Training/final_tweets.csv')

    # print(1)
    # df1 = read_file('/home/dudegrim/Documents/Training/positive_tweets.csv')
    # print(2)
    # df1 = df1.append(read_file('/home/dudegrim/Documents/Training/negative_tweets.csv'), ignore_index=True)
    # print(3)
    # df1 = df1.append(read_file('/home/dudegrim/Documents/Training/neutral_tweets.csv'), ignore_index=True)
    # print(4)
    # df1 = df1.sample(frac=1).reset_index(drop=True)
    # print(5)
    # df1.to_csv('/home/dudegrim/Documents/Training/final_tweets.csv')

    # print(df1['Sentiment'].unique())
    # print(len(df1))

    process(df1, classifier)


start = time.time()
main("NB")
end = time.time()
print(end - start)



