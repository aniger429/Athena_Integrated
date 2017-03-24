from flask import Flask, render_template, send_from_directory, flash, session
from flask import Flask, request, render_template, send_from_directory
from controllers import uploadFile
from controllers.analysis_controller import new_analysis
import os
from DBModels.KBFile import *
from DBModels.Data import *
from DBModels.Username import *
from controllers.DataCleaning import cleaning
from controllers.KnowledgeBaseCreation import *
from controllers.Topic_Analysis import *
from DBModels.MongoDB_Manager import *
import time


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
    print(user_id)
    return render_template("View Data/view_user.html", userData=get_user_data(user_id), user_mentioned_tweet_list=get_user_mentioned_tweets(user_id), tweetDataList=get_user_tweet_data(user_id))


@app.route('/view_tweets')
def view_all_tweets():
    return render_template("View Data/view_tweets.html", tweetFileList=get_all_tweets())


@app.route('/tweet')
def view_specific_tweet():
    tweet_id = request.args.get('tweet_id')
    print(tweet_id)
    return render_template("View Data/view_tweet.html", tweetData=get_tweet_data(tweet_id))


@app.route('/candidate')
def view_candidate_data():
    cname = request.args.get('candidate_name')
    print(cname)
    return render_template("View Data/view_candidate_data.html", candidate_data=get_specific_candidate_names(cname), candidate_tweets=get_candidate_tweets(cname))


@app.route('/topic')
def view_topic_analysis():
    tweets = get_tweets_only()
    tweets = [remove_usernames(t) for t in tweets]
    final_list = tfidf_vectorizer(tweets,1,3)
    lda = topic_lda_tfidf(tweets, 1, 1, 10, 100)
    return render_template("analysis/view_topic_analysis.html", tf_idf=final_list, topics_dict=lda)


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
    start = time.time()
    # This cleans the file selected
    cleaning.cleaning_file(file_path)
    # Updates the data label for isClean
    tweet_cleaned(filename)
    end = time.time()
    print(end - start)
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
    print("here")
    return new_analysis.new_analysis()

    # return redirect(url_for('view_candidate_data'))


if __name__ == '__main__':

    app.run(
        debug=True
    )
