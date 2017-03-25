from afinn import Afinn
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import math
import re
import copy
import pandas as pd
import os
import openpyxl

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "Lexicon_Files")
nltk.data.path.append(script_path+"/Lexicon_Files")

def compute_sentiment(tweet):
    afinn = Afinn()
    filDict = []
    wordList = dict()

    posiFile = pd.read_csv(file_path + "/positive.txt", header=None)
    posi_rowcount, posi_columncount = posiFile.shape
    posi_list = posiFile[0].tolist()
    print(posi_rowcount)
    nega_file = pd.read_csv(file_path + "/negative.txt", header=None)
    nega_rowcount, nega_columncount = nega_file.shape
    nega_list = nega_file[0].tolist()
    print(nega_rowcount)
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

    print('Processing Sentiment Analysis for the word..')
    
    final_sentiment = ''
    
    if (tweet != None):
        original = tweet.lower()
        splitList = original.split()

        # final score
        final_score = 0.0
        # each word in tweet
        for i in range(0, len(splitList)):
            aa = splitList[i]

            pos = 0
            neg = 0
            afinnScore = 0
            WordnetScore = 0
            bingScore = 0
            filScore = 0.0
            if (wordList.get(aa)):
                sentl = wordList.get(aa)
                sentl[1] = 0.0 - sentl[1]
                filScore += sentl[0] + sentl[1]                     

            afinnScore += afinn.score(aa)

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
            """
            sip = swn.senti_synsets(aa)
            sipList = list(sip)
            if len(sipList) > 0:
                for i in range(0, len(sipList)):
                    pos += sipList[i].pos_score()
                    neg += sipList[i].neg_score()
            """
            
            final_score = final_score + bingScore + filScore + afinnScore
            print(aa)
            print('filScore : ' + str(filScore))
            print('Bing : ' + str(bingScore))
            print('Afinn : ' + str(afinnScore))
        
    if (final_score > 0.0):
        final_sentiment = 'POSITIVE'
    elif (final_score < 0.0):
        final_sentiment = 'NEGATIVE'
    elif (final_score == 0.0):
        final_sentiment = 'NEUTRAL'
    print("The final sentiment of the tweet is " + final_sentiment)
    print(str(final_score))
    return final_sentiment
