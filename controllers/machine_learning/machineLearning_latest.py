from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn import model_selection

from sklearn.utils import shuffle
from controllers.machine_learning.cleaning import *
from controllers.analysis_controller import Pickle_Saver as ps
from controllers.DataCleaning import emojip as ep

# save path for classifiers
script_path = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(script_path, "analysis_controller", "Pickles", "ML_Classifier")

# path = 'C:/Users/HKJ/Documents/GitHub/Athena_Integrated/controllers/analysis_controller/Pickles/'

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


print(preprocess("I love banana white frowning face"))

def printouts(data):
    # print out sentiments of input data (such as Election-xx)
    for i in range(0, len(data)):
        print(data['Sentiment'][i])

    # print processed data (includes emoji processed ones)
    # if emojis are processed, they are converted either as 'positiveemoticon' or as 'negativeemoticon'
    for i in range(0, len(data)):
        print(data['Tweet'][i])


def read_file(file_name):
    # data = pd.read_excel(file_name, parse_cols='B,G')
    data_reader = pd.read_csv(file_name, encoding="utf8", keep_default_na=False, sep=",",
                              skipinitialspace=True, chunksize=100, usecols=['Tweet', 'Sentiment'],
                              nrows=1000)
    dataset = pd.DataFrame(columns=['Tweet', 'Sentiment'])

    for chunk in data_reader:
        # this processes the tweets
        chunk['Tweet'] = chunk['Tweet'].apply(lambda x: preprocess(x))
        dataset = dataset.append(chunk, ignore_index=True)

    return dataset


def train(dataX, dataY, index):

    if (index == 1): # Naive Bayes
        text_clf = Pipeline([('vect', TfidfVectorizer(min_df=5, max_df=0.95, use_idf=True, ngram_range=(1, 3))),
                             ('clf', MultinomialNB())])
    elif (index == 2): # SVM
        text_clf = Pipeline([
                             ('vect', TfidfVectorizer(min_df=5, max_df=0.95, use_idf=True, ngram_range=(1, 3))),
                             ('clf', SGDClassifier())
                           ])
    elif (index == 3): # KNN
        text_clf = Pipeline([('vect', TfidfVectorizer(min_df=5, max_df=0.95, use_idf=True, ngram_range=(1, 3))),
                             ('clf', KNeighborsClassifier())])
    elif (index == 4): # Decision Tree
        text_clf = Pipeline([('vect', TfidfVectorizer(min_df=5, max_df=0.95, use_idf=True, ngram_range=(1, 3))),
                             ('clf', DecisionTreeClassifier())])
    elif (index == 5): # Maximum Entropy
        text_clf = Pipeline([('vect', TfidfVectorizer(min_df=5, max_df=0.95, use_idf=True, ngram_range=(1, 3))),
                             ('clf', LogisticRegression())])
    text_clf = text_clf.fit(dataX, dataY)
    
    return text_clf


def process(data):
    # load dataset
    seed = 7
    X = data['Tweet']
    Y = data['Sentiment']
    #test/validation size
    size = 0.2
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=size, random_state=seed)
    print(X_train.shape)
    print(Y_train.shape)
    print(X_validation.shape)
    print(Y_validation.shape)

    # prepare models
    models = []
    models.append(('NB', train(data['Tweet'], data['Sentiment'], 1)))
    models.append(('SVM', train(data['Tweet'], data['Sentiment'], 2)))
    models.append(('KNN', train(data['Tweet'], data['Sentiment'], 3)))
    models.append(('DT', train(data['Tweet'], data['Sentiment'], 4)))
    models.append(('ME', train(data['Tweet'], data['Sentiment'], 5)))

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
    decideSentiment('I love bananas', NB)
    decideSentiment('I love bananas', SVM)
    decideSentiment('I love bananas', KNN)
    decideSentiment('I love bananas', DT)
    decideSentiment('I love bananas', ME)

    # save trained classifiers
    ps.write_pickle(path + '/NB', NB)
    ps.write_pickle(path + '/SVM', SVM)
    ps.write_pickle(path + '/KNN', KNN)
    ps.write_pickle(path + '/DT', DT)
    ps.write_pickle(path + '/ME', ME)


def decideSentiment(tweet, text_clf):  # use this function for sentiment
    a = list()
    a.append(tweet)
    predict = text_clf.predict(a)
    # print(np.mean(predict == data.Sentiment))
    print(tweet)
    print(predict)
    return predict


def main():
    data = pd.DataFrame()

    data = read_file('/home/dudegrim/Documents/Training/positive_tweets.csv')
    data = data.append(read_file('/home/dudegrim/Documents/Training/negative_tweets.csv'), ignore_index=True)
    data = data.append(read_file('/home/dudegrim/Documents/Training/neutral_tweets.csv'), ignore_index=True)
    data = data.sample(frac=1).reset_index(drop=True)

    # printouts(data)
    process(data)

    
# main()
#
#
# NBc = ps.read_pickle(path + '/NB', 'NB')
# SVMc = ps.read_pickle(path + '/SVM', 'SVM')
# KNNc = ps.read_pickle(path + '/KNN', 'KNN')
# DTc = ps.read_pickle(path + '/DT', 'DT')
# MEc = ps.read_pickle(path + '/ME', 'ME')
#
#
# # example.
# decideSentiment('I love bananas', SVMc)
#
