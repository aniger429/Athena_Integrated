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
posi_list = ep.pos_file_to_list()
nega_list = ep.neg_file_to_list()


def preprocess(chunk):
    chunktweet = pd.DataFrame()

    for tweet in chunk:
        print(tweet)
        tweet['Tweet'] = ep.pos(tweet['Tweet'], posi_list)
        tweet['Tweet'] = ep.neg(tweet['Tweet'], nega_list)
        tweet['Tweet'] = data_cleaning(tweet['Tweet'])
        tweet['Tweet'] = removeSp.sub('', tweet['Tweet'])

        chunktweet = chunktweet.append(tweet, ignore_index=True)

    return chunktweet


def read_file(file_name):
    # data = pd.read_excel(file_name, parse_cols='B,G')
    data_reader = pd.read_csv(file_name, encoding = "utf8", keep_default_na = False, index_col = None, sep = ",",
                              skipinitialspace = True, chunksize = 10000, usecols = ['Tweet', 'Sentiment'], nrows=10000)
    dataset = pd.DataFrame()

    for chunk in data_reader:
        dataset = dataset.append(preprocess(chunk), ignore_index=True)

    return dataset


def train(dataX, dataY, index):
    if (index == 1): # Naive Bayes
        text_clf = Pipeline([('vect',TfidfVectorizer(min_df=5, max_df = 0.95, use_idf =True, ngram_range =(1,3))),
                             ('clf',MultinomialNB())])
    elif (index == 2): # SVM
        text_clf = Pipeline([('vect',TfidfVectorizer(min_df=5, max_df = 0.95, use_idf =True, ngram_range =(1,3))),
                             ('clf',SGDClassifier())])
    elif (index == 3): # KNN
        text_clf = Pipeline([('vect',TfidfVectorizer(min_df=5, max_df = 0.95, use_idf =True, ngram_range =(1,3))),
                             ('clf',KNeighborsClassifier())])
    elif (index == 4): # Decision Tree
        text_clf = Pipeline([('vect',TfidfVectorizer(min_df=5, max_df = 0.95, use_idf =True, ngram_range =(1,3))),
                             ('clf',DecisionTreeClassifier())])
    elif (index == 5): # Maximum Entropy
        text_clf = Pipeline([('vect',TfidfVectorizer(min_df=5, max_df = 0.95, use_idf =True, ngram_range =(1,3))),
                             ('clf',LogisticRegression())])
    text_clf = text_clf.fit(dataX,dataY)
    
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
    models.append(('NB', train(data['Tweet'], data['Sentiment'],1)))
    models.append(('SVM', train(data['Tweet'], data['Sentiment'],2)))
    models.append(('KNN', train(data['Tweet'], data['Sentiment'],3)))
    models.append(('DT', train(data['Tweet'], data['Sentiment'],4)))
    models.append(('ME', train(data['Tweet'], data['Sentiment'],5)))
    
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
    ps.write_pickle(path + '/NB', NB)
    ps.write_pickle(path + '/SVM', SVM)
    ps.write_pickle(path + '/KNN', KNN)
    ps.write_pickle(path + '/DT', DT)
    ps.write_pickle(path + '/ME', ME)


def decideSentiment(tweet ,df, text_clf):
    a = []
    a.append(tweet)
    predict = text_clf.predict(a)
    #print(np.mean(predict == data.Sentiment))
    print(tweet)
    print(predict)


data = read_file('/home/dudegrim/Documents/CSV8/Election-18.csv')
print(data)
process(data)
