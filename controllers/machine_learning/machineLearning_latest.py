from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn import model_selection
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score

from controllers.machine_learning.cleaning import *
from controllers.Pickles.Pickle_Saver import *
from controllers.DataCleaning import emojip as ep
from sklearn.externals import joblib
import time

removeSp = re.compile(r'@(\w+)')
posi_list = ep.pos_file_to_list() # get positive list from positive.txt
nega_list = ep.neg_file_to_list() # get negative list from negative.txt


# TODO add comment what each line does


def preprocess(tweet):
    tweet = ep.pos(tweet, posi_list)  # replace all positive emojis (written in positive.txt) to 'POSITIVEEMOTICON'
    tweet = ep.neg(tweet, nega_list)  # replace all negative emojis (written in positive.txt) to 'NEGATIVEEMOTICON'
    tweet = data_cleaning(tweet) # data cleaning and so on.
    tweet = removeSp.sub('', tweet)

    return tweet


def read_file(file_name):
    # data = pd.read_excel(file_name, parse_cols='B,G')
    data_reader = pd.read_csv(file_name, encoding="utf8", keep_default_na=False, sep=",",
                              skipinitialspace=True, chunksize=10000, usecols=['Tweet', 'Sentiment'],
                              nrows=100000)
    dataset = pd.DataFrame(columns=['Tweet', 'Sentiment'])

    for chunk in data_reader:
        # this processes the tweets
        chunk['Tweet'] = chunk['Tweet'].apply(lambda x: preprocess(x))
        dataset = dataset.append(chunk, ignore_index=True)

    return dataset


def train(dataX, dataY, classifier):

    tfidf_vect = TfidfVectorizer(min_df=5, max_df=0.95, use_idf=True, ngram_range=(1, 3))

    if classifier == "NB":  # Naive Bayes
        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', MultinomialNB())])
    elif classifier == "SVM":  # SVM
        text_clf = Pipeline([
                             ('vect', tfidf_vect),
                             ('clf', SGDClassifier(n_jobs=6))
                           ])
    elif classifier == "KNN":  # KNN
        bagging = BaggingClassifier(KNeighborsClassifier(n_neighbors=15, weights='distance'), max_samples=0.5,
                                    max_features=0.5)

        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', bagging)])
    elif classifier == "DT":  # Decision Tree
        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', DecisionTreeClassifier(class_weight='balanced'))])
    else:  # Maximum Entropy
        text_clf = Pipeline([('vect', tfidf_vect),
                             ('clf', LogisticRegression(solver='sag', warm_start=True))])

    text_clf = text_clf.fit(dataX, dataY)
    
    return text_clf


def save_tclf(tclf, index):
    # save path for classifiers
    s_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(s_path, "Pickles", "ML_Classifier")
    joblib.dump(tclf, os.path.join(path, index+'.pkl'))


def process(data, index):
    # load dataset
    seed = 7
    feature = data['Tweet']
    label = data['Sentiment']
    # test/validation size
    size = 0.2
    x_train, x_test, y_train, y_test = model_selection.train_test_split(feature, label,
                                                                        test_size=size, random_state=seed)

    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)

    # train classifiers
    tclf = train(x_train, y_train, 1)

    tclf_pred = tclf.predict(x_test)  # produce predictions

    accuracy = accuracy_score(y_test, tclf_pred, normalize=False)
    print("accuracy")
    print(accuracy)
    report = classification_report(y_test, tclf_pred)  # predictions versus actual ones. this will be printed out as a report.

    print(report)
    print("confusion matrix")
    # Compute confusion matrix
    cnf_matrix = confusion_matrix(y_test, tclf_pred)

    print(cnf_matrix)

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
    data = pd.DataFrame()

    data = read_file('/home/dudegrim/Documents/Training/positive_tweets.csv')
    data = data.append(read_file('/home/dudegrim/Documents/Training/negative_tweets.csv'), ignore_index=True)
    data = data.append(read_file('/home/dudegrim/Documents/Training/neutral_tweets.csv'), ignore_index=True)
    data = data.sample(frac=1).reset_index(drop=True)

    process(data, classifier)


start = time.time()
main("KNN")
end = time.time()
print(end - start)



