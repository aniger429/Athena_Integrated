import pandas as pd
from flask import request, redirect, url_for, render_template
import DBModels
import controllers
import openpyxl


def writeToFile(data, filename):
    d = pd.DataFrame.from_dict(data, orient='columns', dtype=None)
    df = pd.DataFrame(data=d, index=None)
    df.to_excel(filename, index=False)

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

def download():

    which_data = request.form['download_data']
    print("which data:" + which_data)
    filename = ""

    if which_data == "all_usernames":
        data = DBModels.Username.get_dict_list_usernames()
        filename = "Data/Downloads/all_usernames.xlsx"


    elif which_data == "all_candidate_names":
        data = DBModels.KB_Names.get_all_kb_names()
        filename = "Data/Downloads/all_candidate_names.xlsx"

    elif which_data == "download_tweets_candidate":
        data = controllers.analysis_controller.Pickle_Saver.load_obj("Candidate")
        filename = "Data/Downloads/candidate_tweets.xlsx"

    elif which_data == "download_topic_words":
        key = request.form['key']
        data = controllers.analysis_controller.Pickle_Saver.load_obj("Topics")[key]['words']
        filename = "Data/Downloads/topic_"+key+"_keywords.xlsx"

    elif which_data == "download_topic_tweets":
        key = request.form['key']
        data_source = controllers.analysis_controller.Pickle_Saver.load_obj("Topics")[key]['topic_tweets']
        data = [{'tweet': d['tweet'], '_id': str(d['_id'])} for d in data_source]
        filename = "Data/Downloads/topic_"+key+"_tweets.xlsx"

    elif which_data == "download_topic_ngrams":
        data_source = controllers.analysis_controller.Pickle_Saver.load_obj("tf_idf")
        b,c = zip(*(list(data_source.items())))
        data = {'ngram':b, 'score':c}
        filename = "Data/Downloads/topic_ngrams.xlsx"


    writeToFile(data, filename)
    return redirect(redirect_url())


