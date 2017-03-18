from flask import Flask, render_template, send_from_directory, flash, session
from flask import Flask, request, render_template, send_from_directory
from controllers import uploadFile
from controllers.analysis_controller import new_analysis
import os
from DBModels.Data import *
from DBModels.Tweet import *
from DBModels.Username import *
from controllers.DataCleaning import cleaning
from pymodm import connect
import time


# Initialize the Flask application
app = Flask(__name__)

# Connect to MongoDB and call the connection "athenaDB.
connect("mongodb://localhost:27017/Athena", alias="athenaDB")

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'Data/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv', 'xls', 'xlsx'])
app.secret_key = "super secret key"


@app.route('/')
def home():
    session.clear()
    return render_template("dashboard.html", username_count=count_total_usernames(),
                           tweet_count=count_total_tweet(), data_count=count_total_data())


@app.route('/usernames')
def view_all_usernames():
    return render_template("View Data/view_usernames.html", usernameList=get_all_usernames())


@app.route('/user')
def view_specific_user():
    user_id = request.args.get('user_id')
    print(user_id)
    return render_template("View Data/view_user.html", userData=get_user_data(user_id), user_mentioned_tweet_list=get_user_mentioned_tweets(user_id), tweetDataList=get_user_tweet_data(user_id))


@app.route('/tweets')
def view_all_tweets():
    return render_template("View Data/view_tweets.html", tweetFileList=get_all_tweets())


@app.route('/tweet')
def view_specific_tweet():
    tweet_id = request.args.get('tweet_id')
    print(tweet_id)
    return render_template("View Data/view_tweet.html", tweetData=get_tweet_data(tweet_id))


@app.route('/analysis')
def analysis():
    return render_template("analysis.html")


@app.route('/analysis/candidate')
def candidate_analysis():
    return render_template("/analysis/candidate.html")


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


@app.route('/chart-view')
def chart_view():
    return render_template("chart-view.html")

@app.route('/test')
def test():
    return render_template("test.html")


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


@app.route('/new_workspace', methods=['POST'])
def new_workspace():
    return new_analysis.new_analysis()


if __name__ == '__main__':

    app.run(
        debug=True
    )
