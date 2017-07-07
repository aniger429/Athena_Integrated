import pickle
import os
import pandas as pd

script_path = os.path.dirname(os.path.dirname(__file__))


def write_pickle(file_path, obj):
    with open(file_path + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def writeToFile(data, filename):
    d = pd.DataFrame.from_dict(data, orient='columns', dtype=None)
    df = pd.DataFrame(data=d, index=None)
    df.to_csv(filename+".csv", index=False)


def read_pickle(file_path, filename):
    with open(file_path + '.pkl', 'rb') as f:
        cl = pickle.load(f)
        f.close()
    return cl


def save_obj(obj, name):
    file_path = os.path.join(script_path, "analysis_controller", "Pickles", name)
    write_pickle(file_path,obj)

    # #     save tweets
    # if name == "Candidate":
    #     tweets = [{'tweet': d['tweet'], '_id': d['_id']} for d in obj]
    #     file_tweet_path = os.path.join(script_path, "analysis_controller", "Pickles", "Tweets")
    #     write_pickle(file_tweet_path, tweets)

    # writeToFile(obj, file_path)


def load_obj(name):
    file_path = os.path.join(script_path, "analysis_controller", "Pickles", name)
    with open(file_path + '.pkl', 'rb') as f:
        return pickle.load(f)
