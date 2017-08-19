import copy
import os
import re

import nltk
import pandas as pd
from afinn import Afinn
from nltk.corpus import sentiwordnet as swn
from nltk.util import ngrams

from DBModels.Tweet import *

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "Lexicon_Files")
nltk.data.path.append(script_path+"/Lexicon_Files")


def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8', keep_default_na=False)


# this function will return the sentiment of a given word
def compute_sentiment(word):

    return 0


def get_unigrams(tweet):
    return []


def get_bigrams(tweet):
    return []


def get_trigrams(tweet):
    return []


def get_n_grams(tweet_list):
    afinn = Afinn()
    rown = 2
    filDict = []
    unigram = []
    bigram = []
    trigram = []
    final_list = []
    gramDict = dict()    
    wordList = dict()

    posiFile = pd.read_csv(file_path + "/positive.txt", header=None)
    posi_rowcount, posi_columncount = posiFile.shape
    posi_list = posiFile[0].tolist()

    nega_file = pd.read_csv(file_path + "/negative.txt", header=None)
    nega_rowcount, nega_columncount = posiFile.shape
    nega_list = posiFile[0].tolist()

    filDictFile = open(file_path + "/final.txt", 'r', encoding="utf-8")
    filDictCount = len(filDictFile.readlines())
    filDictFile.close()

    filDictFile = open(file_path + "/final.txt", 'r', encoding="utf-8")
    for i in range(0, filDictCount):
        filDict.append(filDictFile.readline())

    filStopFile = open(file_path + "/fil-words.txt", 'r')
    filStopCount = len(filStopFile.readlines())
    filStopFile.close()

    filStopFile = open(file_path + "/fil-words.txt", 'r')
    filsw = dict()
    filscorelist = []
    for i in range(0, filStopCount):
        filsw.update({filStopFile.readline() : 'blank'})

    for i in range(0, filDictCount):
        line = filDict[i]
        if "<positivity>" in line:
            line = line[(line.index(">") + 1) : len(line)]
            filscorelist.append(float(line[0 : line.index("<")]))
        if "<negativity>" in line:
            line = line[(line.index(">") + 1) : len(line)]
            filscorelist.append(float(line[0 : line.index("<")]))
        if "<translation>" in line:
            line = line[(line.index(">") + 1) : len(line)]
            filword = line[0 : line.index("<")]
            if not filword in filsw:
                if len(filscorelist) > 0:            
                    wordList.update({filword : filscorelist})
            filword = ""
            filscorelist = []
            line = filDict[i+1]
            while "<translation>" in line:
                i = i + 1
                line = filDict[i]

    filscorelist = []
    for i in range(0, filDictCount):
        line = filDict[i]
        if "<positivity>" in line:
            line = line[(line.index(">") + 1): len(line)]
            filscorelist.append(float(line[0: line.index("<")]))
        if "<negativity>" in line:
            line = line[(line.index(">") + 1): len(line)]
            filscorelist.append(float(line[0: line.index("<")]))
        if "<translation>" in line:
            for j in range(0, 2):
                i = i + 1
                line = filDict[i]
                if "<translation>" in line:
                    line = line[(line.index(">") + 1): len(line)]
                    filword = line[0: line.index("<")]
                    if not filword in wordList:
                        if len(filscorelist) > 0:            
                            wordList.update({filword: filscorelist})
                else:
                    break       
            line = filDict[i+1]
            while "<translation>" in line:
                i = i + 1
                line = filDict[i]
            filscorelist = []

    print('Filipino Dictionary loaded.')
    print('Processing Sentiment Analysis for each words..')
    rown = 0
    for tweet in tweet_list:
            rown += 1
            if (tweet != None):
                print('Processing Tweet ' + str(rown))
                # remove username mentions in tweet body
                if '@' in original:
                    original = original.replace('@', '')
                splitList = original.split()

                # filipino word sentiment
                filScore = 0.0

                # each word in tweet
                for i in range(0, len(splitList)):
                    # word in tweet
                    aa = splitList[i]

                    if '[' in aa:
                        aa = aa.replace('[', '')
                        if ']' in aa:
                            aa = aa.replace(']', '')

                    deleteChecker = 0
                    filipinoChecker = 0
                    pos = 0
                    neg = 0
                    eachScore = 0
                    afinnScore = 0
                    WordnetScore = 0
                    bingScore = 0
                    if (wordList.get(aa)):
                        sentl = wordList.get(aa)
                        sentl[1] = 0.0 - sentl[1]
                        filScore += sentl[0] + sentl[1]
                        eachScore = sentl[0] + sentl[1]                       
                    if (eachScore > 0.0) or (eachScore < 0.0):
                        filipinoChecker = 1
                    afinnScore += afinn.score(aa)
                    if (afinnScore == 0.0):
                        deleteChecker += 1

                    # if aa in posi_list:
                    #     bingScore += 1

                    posiFile = open(file_path + "/positive.txt", 'r')
                    for j in range(0, posi_rowcount):
                        idRead = posiFile.readline()
                        idSplice = idRead.split()
                        if aa == idSplice[0]:
                            bingScore += 1
                    posiFile.close()
                    negaFile = open(file_path + "/negative.txt", 'r')
                    for j in range(0, nega_rowcount):
                        idRead2 = negaFile.readline()
                        idSplice2 = idRead2.split()
                        if aa == idSplice2[0]:
                            bingScore -= 1

                    # if aa in nega_list:
                    #     bingScore -= 1

                    if (bingScore == 0.0):
                        deleteChecker += 1
                    sip = swn.senti_synsets(aa)
                    sipList = list(sip)
                    if len(sipList) > 0:
                        for i in range(0, len(sipList)):
                            pos += sipList[i].pos_score()
                            neg += sipList[i].neg_score()
                    if ((pos - neg) == 0.0):
                        deleteChecker += 1                        
                    if (deleteChecker >= 2) and (filipinoChecker == 0):
                        original = re.sub(r'\b' + aa + r'\b', '', original)
                        
                uni = ngrams(original.split(),1)
                unigram = [' '.join(words) for words in uni]
                bi = ngrams(original.split(),2)
                bigram = [' '.join(words) for words in bi]
                tri = ngrams(original.split(),3)
                trigram = [' '.join(words) for words in tri]

                gramDict['unigram'] = unigram
                gramDict['bigram'] = bigram
                gramDict['trigram'] = trigram
                final_list.append(copy.deepcopy(gramDict))
                gramDict.clear()
                
    
    print("done.")
    return final_list

# import xml.etree.ElementTree as ET
# from lxml import etree
# import pandas as pd
#
# xml_data = file_path + "/final - Copy.xml"
#
# def xml2df(xml_data):
#     tree = ET.parse(xml_data)
#     root = tree.getroot()
#     all_records = []
#     headers = []
#     for i, child in enumerate(root):
#         record = []
#         for subchild in child:
#             record.append(subchild.text)
#             if subchild.tag not in headers:
#                 headers.append(subchild.tag)
#         all_records.append(record)
#     return pd.DataFrame(all_records, columns=headers)
#
#
# xml_file = xml2df(xml_data)
#
# for x in xml_file[:10]:
#     print (x)


dum_data = get_tweets_only()
output = get_n_grams(dum_data)
df_output = pd.DataFrame.from_dict(output)
df_output.to_excel("feprocessed.xlsx", index=False, header=['Bigram', 'Trigram', 'Unigram'])
