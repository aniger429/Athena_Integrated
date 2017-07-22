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


def save_dataframe(df, name):
    file_path = os.path.join(script_path, "Pickles", "Data", name+".pkl")
    df.to_pickle(file_path)
    return


def load_pickled_dataframe(name):
    file_path = os.path.join(script_path, "Pickles", "Data", name+".pkl")
    return pd.read_pickle(file_path)


def save_obj(obj, name):
    file_path = os.path.join(script_path, "Pickles", name)
    write_pickle(file_path, obj)


def load_obj(name):
    file_path = os.path.join(script_path, "Pickles", name)
    with open(file_path + '.pkl', 'rb') as f:
        return pickle.load(f)

