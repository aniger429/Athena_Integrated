from afinn import Afinn
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import math
import re
import csv
import copy

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
    posiFile = open("C:/Python27/positive.txt", 'r');
    posiCount = len(posiFile.readlines())
    posiFile.close();
    negaFile = open("C:/Python27/negative.txt", 'r');
    negaCount = len(negaFile.readlines())
    negaFile.close();
    filDictFile = open("C:/Python27/src/final.txt", 'r', encoding="utf-8");
    filDictCount = len(filDictFile.readlines())
    filDictFile.close();
    filDictFile = open("C:/Python27/src/final.txt", 'r', encoding="utf-8");
    for i in range(0, filDictCount):
        filDict.append(filDictFile.readline())
        
    filStopFile = open("C:/Python27/src/fil-words.txt", 'r');
    filStopCount = len(filStopFile.readlines())
    filStopFile.close();
    filStopFile = open("C:/Python27/src/fil-words.txt", 'r');
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
            line = filDict[i+1];
            while "<translation>" in line:
                i = i + 1
                line = filDict[i]

    filscorelist = []
    for i in range(0, filDictCount):
        line = filDict[i]
        if "<positivity>" in line:
            line = line[(line.index(">") + 1) : len(line)]
            filscorelist.append(float(line[0 : line.index("<")]))
        if "<negativity>" in line:
            line = line[(line.index(">") + 1) : len(line)]
            filscorelist.append(float(line[0 : line.index("<")]))
        if "<translation>" in line:
            for j in range(0, 2):
                i = i + 1;
                line = filDict[i]
                if "<translation>" in line:
                    line = line[(line.index(">") + 1) : len(line)]
                    filword = line[0 : line.index("<")]
                    if not filword in wordList:
                        if len(filscorelist) > 0:            
                            wordList.update({filword : filscorelist})
                else:
                    break;       
            line = filDict[i+1];
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
                original = tweet.lower()
                if '@' in original:
                    original = original.replace('@', '')
                splitList = original.split()
                aa = ""
                filScore = 0.0
                for i in range(0, len(splitList)):
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
                    posiFile = open("C:/Python27/positive.txt", 'r');
                    for j in range(0, posiCount):
                        idRead = posiFile.readline()
                        idSplice = idRead.split()
                        if aa == idSplice[0]:
                            bingScore += 1
                    posiFile.close()
                    negaFile = open("C:/Python27/negative.txt", 'r');
                    for j in range(0, negaCount):
                        idRead2 = negaFile.readline()
                        idSplice2 = idRead2.split()
                        if aa == idSplice2[0]:
                            bingScore -= 1
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

