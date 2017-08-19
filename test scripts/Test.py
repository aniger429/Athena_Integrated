import os
import re
import timeit

import pandas as pd

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "controllers", "stop_words")


def test1():
    stopwords = pd.read_csv(file_path+"/eng-function-word.txt", header=None)
    stopwords = stopwords.append(pd.read_csv(file_path+"/fil-function-words.txt", header=None))
    stopwords = stopwords[0].tolist()
    stopwords = [x.lower() for x in stopwords]

    stopwords = [re.sub('\'|"| ', '', x) for x in stopwords]


def test2():
    script_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(script_path, "controllers", "stop_words")

    stopwords = pd.read_csv(file_path+"/eng-function-word.txt", header=None)
    stopwords = stopwords.append(pd.read_csv(file_path+"/fil-function-words.txt", header=None))
    stopwords = stopwords[0].tolist()
    stopwords = [x.lower() for x in stopwords]

    stopwords = [re.sub('\'|"| ', '', x) for x in stopwords]
    df = pd.DataFrame(stopwords)
    df.to_csv(os.path.join(file_path, "final_stop_words_list.csv"), header=None, index=None)


def test3():
    stopwords = pd.read_csv(file_path+"/final_stop_words_list.csv", header=None, squeeze=True).tolist()


print(timeit.timeit(test1, number=100))
print(timeit.timeit(test3, number=100))

