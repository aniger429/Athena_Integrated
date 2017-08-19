import unicodedata as uni
from os import path

import pandas as pd

# as of unicodedata version 8.0.0

script_path = path.dirname(path.dirname(__file__))
txt_path = path.join(script_path, 'DataCleaning')


def pos_file_to_list():
    posiFile = pd.read_csv(txt_path+"/positive.txt", header=None)
    posi_list = posiFile[0].tolist()
    return posi_list


def neg_file_to_list():
    nega_file = pd.read_csv(txt_path+"/negative.txt", header=None)
    nega_list = nega_file[0].tolist()
    return nega_list


def pos(string, posi_list):
    for i in range(0, len(posi_list)):
        if uni.lookup(posi_list[i]) in string:
            string = string.replace(uni.lookup(posi_list[i]), ' POSITIVEEMOTICON ')
    return string


def neg(string, nega_list):
    for i in range(0, len(nega_list)):
        if uni.lookup(nega_list[i]) in string:
            string = string.replace(uni.lookup(nega_list[i]), ' NEGATIVEEMOTICON ')
    return string


def noPos(string):
    no = 0
    while 'positiveemoticon' in string:
        string = string.replace('positiveemoticon', '', 1)
        no += 1
    return no


def noNeg(string):
    no = 0
    while 'negativeemoticon' in string:
        string = string.replace('negativeemoticon', '', 1)
        no += 1
    return no

