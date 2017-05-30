from flask import Flask, request, render_template
from flask import session

from DBModels.Data import *
from DBModels.KBFile import *
from DBModels.MongoDB_Manager import *
from DBModels.Username import *
from controllers import uploadFile
from controllers.Candidate_Analysis.Candidate_Identification_Final import *
from controllers.DataCleaning import cleaning
from controllers.KnowledgeBaseCreation import *
from controllers.Sentiment_Analysis.Sentiment_Identification import *
from controllers.Topic_Analysis.Find_Topic_Tweets import *
from controllers.Topic_Analysis.Topic_Analysis import *
from controllers.analysis_controller import new_analysis
from controllers.analysis_controller.Pickle_Saver import *
from collections import Counter

# Initialize the Flask application
app = Flask(__name__)

# Connect to MongoDB and call the connection "athenaDB.
# connect("mongodb://localhost:27017/Athena", alias="athenaDB")

client = MongoClient('localhost', 27017)
mainDB = "Athena"
db = client[mainDB]

# create the main database
create_new_workspace(mainDB)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'Data/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv', 'xls', 'xlsx'])
app.secret_key = "super secret key"


@app.route('/')
def home():
    session.clear()
    return render_template("dashboard.html", counter_data=[count_total_usernames(),count_total_tweet(),count_total_candidate(),count_total_data(),count_total_workspace()], counter_names = ["username","tweet","candidate","file","workspace"])


@app.route('/view_workspaces')
def view_all_workspaces():
    return render_template("View Data/view_workspaces.html", workspaceList=get_all_workspace())


@app.route('/view_usernames')
def view_all_usernames():
    return render_template("View Data/view_usernames.html", usernameList=get_all_usernames())


@app.route('/user')
def view_specific_user():
    user_id = request.args.get('user_id')
    return render_template("View Data/view_user.html", userData=get_user_data(user_id), user_mentioned_tweet_list=get_user_mentioned_tweets(user_id), tweetDataList=get_user_tweet_data(user_id))


@app.route('/view_tweets')
def view_all_tweets():
    return render_template("View Data/view_tweets.html", tweetFileList=get_all_tweets())


@app.route('/tweet')
def view_specific_tweet():
    tweet_id = request.args.get('tweet_id')
    return render_template("View Data/view_tweet.html", tweetData=get_tweet_data(tweet_id))


@app.route('/candidate')
def view_candidate_data():
    cname = request.args.get('candidate_name')
    datasource = request.args.get('datasource')

    tweets = get_all_tweets()

    if datasource in ["positive", "neutral", "negative"]:
        tweets = load_obj("Sentiment")[datasource]
    elif datasource == "topic":
        key = request.args.get('key')
        tweets = load_obj("Topics")[key]['topic_tweets']
        print(tweets)

    identify_candidate(tweets, cname=cname)
    data = load_obj("Candidate")
    candidate_name_count = Counter([tweet['tweet'][tweet['cand_ana'][cname]] for tweet in data])

    return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count, candidate_data=get_specific_candidate_names(cname),
                           candidate_tweets=data)


@app.route('/topic')
def view_topic_analysis():
    tweets = get_all_tweets()
    datasource=request.args.get('datasource')
    topic_for = "All Tweets"

    if datasource == "candidate":
        cname = request.args.get('candidate_name')
        # tweets = [d for d in load_obj("Candidate") if d['cand_ana'][cname] != '-1']
        tweets = load_obj("Tweets")
        topic_for = "Candidate: "+cname
    elif datasource == "sentiment":
        senti = request.args.get('senti')
        data = load_obj("Sentiment")
        topic_tweets = data[senti]
        topic_for=senti+"Sentiment"

    tweets_only = [remove_usernames(t['tweet']) for t in tweets]
    final_list = tfidf_vectorizer(tweets_only, 1, 3)
    lda = topic_lda_tfidf(tweets_only, 1, 1, 10, 100)
    find_topic_tweets(lda,tweets)

    return render_template("analysis/Topic/view_topic_analysis.html", tf_idf=final_list, topics_dict=lda,
                           topic_analysis_for=topic_for)

@app.route('/topic_tweets')
def view_tweets_for_topic():
    key = request.args.get('key')
    data = load_obj("Topics")
    candidates_mentioned = identify_candidate_mentioned(data[key]['topic_tweets'])
    return render_template("analysis/Topic/view_topic_tweets.html", key=key, topic=data[key], candidates_mentioned=candidates_mentioned)


@app.route('/sentiment')
def view_sentiment_analysis():
    tweets = get_all_tweets()
    datasource = request.args.get('datasource')
    sentiment_for = "All"

    if datasource == "Topic":
        key = request.args.get('key')
        tweets = load_obj("Topics")[key]['topic_tweets']
        sentiment_for = "Topic # "+key

    elif datasource == "Candidate":
        candidate_name = request.args.get('candidate_name')
        tweets = load_obj("Tweets")
        sentiment_for="Candidate: "+candidate_name

    positive_tweets, neutral_tweets, negative_tweets = compute_tweets_sentiment(tweets)

    positive_tweets = {'tweets': positive_tweets, 'candidate_mentioned': identify_candidate_mentioned(positive_tweets)}
    neutral_tweets = {'tweets': neutral_tweets, 'candidate_mentioned': identify_candidate_mentioned(neutral_tweets)}
    negative_tweets = {'tweets': negative_tweets, 'candidate_mentioned': identify_candidate_mentioned(negative_tweets)}

    return render_template("analysis/view_tweets_sentiment.html", tweet_list=[negative_tweets, positive_tweets,neutral_tweets], sentiment_labels=['negative', 'neutral', 'positive'], sentiment_analysis_for=sentiment_for)


@app.route('/analysis')
def analysis():
    return render_template("analysis.html", candidate_names=get_all_candidate_names(), workspace_list=get_all_workspace())


@app.route('/data_cleaning')
def data_cleaning():
    return render_template("datacleaning.html", dataFileList=get_all_file(), duplicate = False)


@app.route('/data_cleaning/<filename>')
def clean_file(filename):
    script_path = os.path.dirname(__file__)
    file_path = os.path.join(script_path, app.config['UPLOAD_FOLDER'], filename)
    # This cleans the file selected
    cleaning.cleaning_file(file_path)
    # Updates the data label for isClean
    tweet_cleaned(filename)
    return render_template("datacleaning.html", dataFileList=get_all_file())


@app.route('/knowledgebase')
def knowledge_base():
    return render_template("knowledgebase.html", kb_name_list=get_all_kb_names(), kbFileList=get_all_kbfile(), duplicate=False)


@app.route('/chart-view')
def chart_view():
    return render_template("chart-view.html")


@app.route('/test')
def test():
    return render_template("base.html")


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_name = file.filename
    if check_if_file_exists(file_name) is False:
        script_path = os.path.dirname(__file__)
        directoryPath = os.path.join(script_path, app.config['UPLOAD_FOLDER'])
        return uploadFile.upload(directoryPath, app.config['ALLOWED_EXTENSIONS'])
    else:
        return render_template("datacleaning.html", dataFileList=get_all_file(), filename = file_name, duplicate = True)


# Route that will process the file upload
@app.route('/kbupload', methods=['POST'])
def kbupload():
    file = request.files['file']
    file_name = file.filename
    if check_if_kbfile_exists(file_name) is False:
        script_path = os.path.dirname(__file__)
        directoryPath = os.path.join(script_path, app.config['UPLOAD_FOLDER'], "KBFiles")
        return uploadFile.kbupload(directoryPath, app.config['ALLOWED_EXTENSIONS'])
    else:
        return render_template("knowledgebase.html", kbFileList=get_all_kbfile(), filename = file_name, duplicate = True)


@app.route('/kbupdate')
def find_more_kb_names():
    find_more_names()
    return render_template("knowledgebase.html", kb_name_list=get_all_kb_names(), kbFileList=get_all_kbfile(), duplicate=False)


@app.route('/new_workspace', methods=['POST'])
def new_workspace():
    return render_template("analysis/analysis_processing.html")

    # return new_analysis.new_analysis()


if __name__ == '__main__':
    app.run(
        debug=True
    )
