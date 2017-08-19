import itertools
import time
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from controllers.Sentiment_Analysis.Sentiment_Identification import *
from controllers.machine_learning.cleaning import *


def read_file(file_name):
    data_reader = pd.read_csv(file_name, encoding="utf8", keep_default_na=False, sep=",",
                              skipinitialspace=True, chunksize=15000, usecols=['Tweet', 'Sentiment'])
    dataset = pd.DataFrame(columns=['Tweet', 'Sentiment'])

    for chunk in data_reader:
        # this processes the tweets
        dataset = dataset.append(clean_tweets_multiprocess(chunk), ignore_index=True)

    # remove tweets that are empty after processing
    dataset = dataset[dataset.Tweet != '']
    # remove data with no sentiment identified
    dataset = dataset[dataset.Sentiment != '']

    return dataset

def classifiers(classifier):
    s_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(s_path, "controllers", "Pickles", "ML_Classifier")

    if classifier == "NB":  # Naive Bayes
        print("NB")
        clf = pickle.load(open(path+'/NB.pkl', 'rb'))

    elif classifier == "SVM":  # SVM
        print("SVM")
        clf = pickle.load(open(path + '/SVM.pkl', 'rb'))
    elif classifier == "KNN":  # KNN
        print("KNN")

    elif classifier == "DT":  # Decision Tree
        print("DT")
        clf = pickle.load(open(path + '/DT.pkl', 'rb'))
    elif classifier == "PAC":
        print("PAC")
        clf = pickle.load(open(path + '/PAC.pkl', 'rb'))
    elif classifier == "LSVC":
        print("LSVC")
        clf = pickle.load(open(path + '/LSVC.pkl', 'rb'))
    else:  # Maximum Entropy
        print("ME")
        clf = pickle.load(open(path + '/ME.pkl', 'rb'))

    return clf


def plot_confusion_matrix(dataset, cm, classes,
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

    plt.savefig('/home/dudegrim/Documents/Testing/postdefense/dataset'+str(dataset)+'/'+title+'.png', bbox_inches='tight')


def show_results(dataset_num, clf_pred, label_test, index):
    accuracy = accuracy_score(label_test, clf_pred)
    print("accuracy")
    print(accuracy)
    report = classification_report(label_test, clf_pred)  # predictions versus actual ones. this will be printed out as a report.

    print(report)
    print("confusion matrix")
    cnf_matrix = confusion_matrix(label_test, clf_pred, labels=["Positive", "Neutral", "Negative"])
    np.set_printoptions(precision=2)

    print(cnf_matrix)

    plt.figure()
    plot_confusion_matrix(dataset_num, cnf_matrix, classes=["Positive", "Neutral", "Negative"], normalize=True,
                          title=index + ' Normalized confusion matrix')


def lexicon_based(tweet):
    return sa_parallelize_dataframe(tweet, lexicon_sentiment)


def testing(index, dataset_num):
    print(index, dataset_num)
    df1 = read_file('/home/dudegrim/Documents/Testing/postdefense/dataset'+str(dataset_num)+'.csv')
    # clf = classifiers(index)


    positive = df1[df1['Sentiment'] == "Positive"].head(100000)
    negative = df1[df1['Sentiment'] == "Negative"].head(100000)
    neutral = df1[df1['Sentiment'] == "Neutral"].head(100000)

    final = positive.append(negative)
    final = final.append(neutral)

    final = final.sample(frac=1).reset_index(drop=True)


    # print(final)
    # print(len(final[final['Sentiment'] == "Positive"]))
    # print(len(final[final['Sentiment'] == "Neutral"]))
    # print(len(final[final['Sentiment'] == "Negative"]))

    data_test = list(final['Tweet'])
    label_test = list(final['Sentiment'])

    # predict sentiment
    # clf_pred = clf.predict(data_test)  # produce predictions
    clf_pred = lexicon_based(final)

    # show results
    # show_results(dataset_num, clf_pred, label_test, index)
    show_results(dataset_num, clf_pred['Sentiment_LB'], label_test, index)



start = time.time()
# NB, SVM, DT, PAC, LSVC, ME, LB
testing('LB', 3)
end = time.time()
print(end - start)
