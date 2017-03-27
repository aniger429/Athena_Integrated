import pickle
import os

script_path = os.path.dirname(os.path.dirname(__file__))


def write_pickle(file_path, obj):
    with open(file_path + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def save_obj(obj, name):
    file_path = os.path.join(script_path, "analysis_controller", "Pickles", name)
    write_pickle(file_path,obj)

    #     save tweets
    if name == "Candidate":
        tweets = [{'tweet': d['tweet'], '_id': d['_id']} for d in obj]
        file_tweet_path = os.path.join(script_path, "analysis_controller", "Pickles", "Tweets")
        write_pickle(file_tweet_path, tweets)


def load_obj(name):
    file_path = os.path.join(script_path, "analysis_controller", "Pickles", name)
    with open(file_path + '.pkl', 'rb') as f:
        return pickle.load(f)
