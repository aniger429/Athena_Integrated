import pickle
import os

script_path = os.path.dirname(os.path.dirname(__file__))


def save_obj(obj, name):
    file_path = os.path.join(script_path, "Topic_Analysis", name)
    with open(file_path + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    file_path = os.path.join(script_path, "Topic_Analysis", name)
    with open(file_path + '.pkl', 'rb') as f:
        return pickle.load(f)
