from flask import Flask, render_template, send_from_directory
from controllers import uploadFile
import os
from DBModels.Data import *
from DBModels.Tweet import *
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

@app.route('/')
def home():
    return render_template("base.html")

@app.route('/tweets')
def view_tweets():
    return render_template("tweets.html", tweetFileList=get_all_tweets())


@app.route('/analysis')
def analysis():
    return render_template("analysis.html")

@app.route('/analysis/candidate')
def candidate_analysis():
    return render_template("/analysis/candidate.html")


@app.route('/data_cleaning')
def data_cleaning():
    return render_template("datacleaning.html", dataFileList=get_all_file())


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


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    script_path = os.path.dirname(__file__)
    directoryPath = os.path.join(script_path, app.config['UPLOAD_FOLDER'])
    return uploadFile.upload(directoryPath, app.config['ALLOWED_EXTENSIONS'])


if __name__ == '__main__':
    app.run(
        debug=True
    )
