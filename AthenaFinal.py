from flask import Flask, send_from_directory
from flask import session

from DBModels.Data import *
from DBModels.KBFile import *
from DBModels.MongoDB_Manager import *
from DBModels.Username import *
from DBModels.Lexicon import *
from controllers import uploadFile
from controllers.DataCleaning import cleaning
from controllers.KnowledgeBaseCreation import *
from controllers.download import *
from controllers.analysis_controller.topic_view_analysis import *
from controllers.analysis_controller.analysis_manager import new_analysis
from controllers.visualization.donut_chart import *
from controllers.init_athena import *

# Initialize the Flask application
app = Flask(__name__)
# app.jinja_env.filters['b64d'] = lambda u: b64encode(u).decode()

# db = MongoClient('localhost', 27017).Athena

# create the main database
create_new_workspace(mainDB)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'Data/'
app.config['MEDIA_FOLDER'] = 'media_folder/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv', 'xls', 'xlsx'])
app.secret_key = "super secret key"


@app.route('/')
def home():
    session.clear()
    return render_template("dashboard.html", counter_data=[count_total_usernames(),count_total_tweet(),
                                                           count_total_candidate(),count_total_data()],
                           counter_names=["username", "tweet", "candidate", "file"])


@app.route('/view_workspaces')
def view_all_workspaces():
    return render_template("View Data/view_workspaces.html", workspaceList=get_all_workspace())


@app.route('/view_usernames')
def view_all_usernames():
    return render_template("View Data/view_usernames.html", usernameList=get_all_usernames(100),
                           total_usernames=count_total_usernames())


@app.route('/user')
def view_specific_user():
    user_id = request.args.get('user_id')
    return render_template("View Data/view_user.html", userData=get_user_data(user_id),
                           user_mentioned_tweet_list=get_user_mentioned_tweets(user_id),
                           tweetDataList=get_user_tweet_data(user_id))


@app.route('/view_tweets')
def view_all_tweets():
    return render_template("View Data/view_tweets.html", tweetFileList=get_all_orig_tweets(1000),
                           total_tweet=count_total_tweet())


@app.route('/tweet')
def view_specific_tweet():
    tweet_id = request.args.get('tweet_id')
    return render_template("View Data/view_tweet.html", tweetData=get_tweet_data(tweet_id))


@app.route('/delete_candidate_names', methods=['POST'])
def delete_candidate_names():
    candidate = request.form['candidate_name']
    names = request.form.getlist('names[]')
    delete_kb_names(names, candidate)
    return redirect(redirect_url())


@app.route('/add_candidate_names', methods=['POST'])
def add_candidate_names():
    candidate = request.form['candidate_name']
    names = request.form['add_names'].split(",")
    new_kb_names(names, candidate)
    return redirect(redirect_url())


@app.route('/candidate_names')
def view_candidate_names():
    cname = request.args.get('candidate_name')

    return render_template("View Data/view_candidate_names.html", candidate_data=get_specific_candidate_names(cname))


@app.route('/candidate')
def view_candidate_data():
    cname = request.args.get('candidate_name')
    datasource = request.args.get('datasource')

    tweets = get_all_tweets()
    # tweets = get_all_orig_tweets()

    if datasource in ["positive", "neutral", "negative"]:
        tweets = load_pickled_dataframe(datasource)
    elif datasource == "topic":
        key = request.args.get('key')
        tweets = load_obj("Topics")[key]['topic_tweets']

    candidate_name_count, data_tweets = candidate_analysis(tweets, cname)

    return render_template("View Data/view_candidate_data.html", candidate_name_count=candidate_name_count,
                           candidate_data=get_specific_candidate_names(cname),
                           candidate_tweets=data_tweets)


@app.route('/topic_analysis_manager', methods=['POST'])
# this calls the view_analysis under controllers folder
def topic_analysis_manager():
    datasource = request.form['datasource']
    print(datasource)
    # source: candidate
    if datasource == "candidate":
        candidate_name = request.form['candidate_name']
        return view_candidate(candidate_name)
    # source: sentiment
    elif datasource == "sentiment":
        sentiment = request.form['sentiment']
        return view_sentiment(sentiment)


@app.route('/topic_tweets')
def view_tweets_for_topic():
    key = request.args.get('key')
    data = load_obj("Topics")
    tweet_df = data[key]['topic_tweets']
    candidates_mentioned = identify_candidate_mentioned(tweet_df)
    return render_template("analysis/Topic/view_topic_tweets.html", key=key, topic=data[key],
                           candidates_mentioned=candidates_mentioned)


@app.route('/sentiment')
def view_sentiment_analysis():
    tweets = get_all_orig_tweets()
    datasource = request.args.get('datasource')
    sentiment_for = "All"

    if datasource == "Topic":
        key = request.args.get('key')
        tweets = load_obj("Topics")[key]['topic_tweets']
        sentiment_for = "Topic # "+key

    elif datasource == "Candidate":
        candidate_name = request.args.get('candidate_name')
        tweets = load_pickled_dataframe("Candidate")
        sentiment_for = "Candidate: " + candidate_name

    positive_tweets, neutral_tweets, negative_tweets = compute_tweets_sentiment(tweets)

    positive_tweets = {'tweets': positive_tweets, 'candidate_mentioned': identify_candidate_mentioned(positive_tweets)}
    neutral_tweets = {'tweets': neutral_tweets, 'candidate_mentioned': identify_candidate_mentioned(neutral_tweets)}
    negative_tweets = {'tweets': negative_tweets, 'candidate_mentioned': identify_candidate_mentioned(negative_tweets)}

    data_series = pd.Series([len(positive_tweets['tweets']), len(neutral_tweets['tweets']),
                             len(negative_tweets['tweets'])],
                            index=['Neutral', 'Positive', 'Negative'])

    script, div = donut_chart(data_series)

    return render_template("analysis/Sentiment/view_tweets_sentiment.html",
                           tweet_list=[negative_tweets, positive_tweets, neutral_tweets],
                           sentiment_labels=['negative', 'neutral', 'positive'],
                           sentiment_analysis_for=sentiment_for,
                           script=script, div=div)


@app.route('/analysis')
def analysis():
    return render_template("analysis.html", candidate_names=get_all_candidate_names(),
                           workspace_list=get_all_workspace())


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
    return render_template("knowledgebase.html", kb_name_list=get_all_kb_names(),
                           kbFileList=get_all_kbfile(), duplicate=False)


@app.route('/populate_lexicons', methods=['POST'])
def populate_lexicons():
    # populate the lexicon base
    populate_lexicon()
    return redirect(redirect_url())


@app.route('/view_lexicon')
def view_lexicon():
    return render_template("lexicon/view_all_lexicons.html", all_lexicon=get_all_lexicon())

@app.route('/view_lexicon_words', methods=['GET'])
def view_lexicon_words():
    language = request.args.get('language')
    sentiment = request.args.get('sentiment')
    return render_template("lexicon/lexicon_base.html", sentiment_words=get_all_words(language, sentiment), sentiment=sentiment, language=language)


@app.route('/delete_lexicon_word', methods=['POST'])
def delete_lexicon_word():
    language = request.form['language']
    sentiment = request.form['sentiment']
    names = request.form.getlist('names[]')
    delete_lexicon_words(names, language, sentiment)
    return redirect(redirect_url())


@app.route('/add_lexicon_words', methods=['POST'])
def add_lexicon_words():
    language = request.form['language']
    sentiment = request.form['sentiment']
    names = request.form['add_names'].split(",")
    new_lexicon_words(names, language, sentiment)
    return redirect(redirect_url())


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
        return render_template("datacleaning.html", dataFileList=get_all_file(),
                               filename=file_name, duplicate=True)


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
        return render_template("knowledgebase.html", kbFileList=get_all_kbfile(),
                               filename=file_name, duplicate=True)


@app.route('/kbupdate')
def find_more_kb_names():
    find_more_names()
    return render_template("knowledgebase.html", kb_name_list=get_all_kb_names(),
                           kbFileList=get_all_kbfile(), duplicate=False)


@app.route('/analysis_config', methods=['POST'])
def analysis_config():
    flevel = request.form['first-level']
    slevel = request.form['second-level']
    tlevel = request.form['third-level']
    last = ""
    vizOptions = []
    count= 5
    if tlevel == "none":
        if slevel == "none":
            last = flevel;
            count = 3
        else:
            count = 4
            last = slevel
    else:
        last = tlevel

    if last == "candidate":
        vizOptions = ['concordancer']
    elif last == "topic":
        vizOptions = ['default']
    elif last == "sentiment":
        vizOptions = ['Tabular VIew']
        if flevel == "candidate" or slevel == "candidate":
            vizOptions.append("Concordancer with Sentiment")

    return render_template("analysis/analysis_processing.html",
                           candidate_names=get_all_candidate_names(), flevel=flevel, slevel=slevel, tlevel=tlevel,
                           vizOptions=vizOptions, count=count)


@app.route('/new_analysis', methods=['POST'])
def new_ana():
    return new_analysis()


@app.route('/download', methods=['POST'])
def download_data():
    return download()


@app.route('/visualization', methods=['POST'])
def visualizations():
    viz_type = request.form['viz_type']


@app.route('/get_word_cloud')
def get_word_cloud():
    filename = "word_cloud.png"
    return send_from_directory(app.config['MEDIA_FOLDER'], filename, as_attachment=True)


# Bokeh Visualizations
@app.route('/test')
def test_bokeh():
    # data = [{'name': "C1", 'population': [1,2,3]},
    #         {'name': "C2", 'population': [4, 5, 9]}]
    data = [
               ('State','Under 5 Years','5 to 13 Years','14 to 17 Years','18 to 24 Years','25 to 44 Years',
         '45 to 64 Years','65 Years and Over'),
           ('AL',310504,552339,259034,450818,1231572,1215966,641667),
    ('AK',52083,85640,42153,74257,198724,183159,50277)
    ]
    return render_template('test.html', data=data)


@app.route('/view_graph', methods=['GET'])
def view_graph():
    import json
    script_path = os.path.dirname(__file__)
    json_url = os.path.join(script_path, "controllers", "graphs.json")
    jsondata = json.load(open(json_url))
    return render_template('analysis/Topic/view_scatterplot.html', jsondata=jsondata)


if __name__ == '__main__':
    app.run(
        debug=True
    )
