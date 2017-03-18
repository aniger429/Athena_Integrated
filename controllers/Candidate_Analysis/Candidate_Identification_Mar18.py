import json
import pandas as pd
import copy
import csv
import re
from collections import defaultdict

def identify_candidate(tweet_list):
    knowledgeBase = open('C:/Users/HKJ/AppData/Local/Programs/Python/Python35/KnowledgeBase.txt', 'r')
    lineCount = len(knowledgeBase.readlines())
    knowledgeBase.close();
    knowledgeBase = open('C:/Users/HKJ/AppData/Local/Programs/Python/Python35/KnowledgeBase.txt', 'r')

    nameList = []
    duterteList = []
    binayList = []
    poeList = []
    roxasList = []
    santiagoList = []
    nickDict = defaultdict(list)
        

    for i in range(0, lineCount):
        names = knowledgeBase.readline().split(':')
        nick = names[1]
        nickname = re.sub(r"[\[\]\"\'\n]", "", nick)
        nickDict[names[0]].append(nickname)
    duterteList = duterteList + nickDict['Rodrigo'] + nickDict['Digong'] + nickDict['Du30'] + nickDict['Duterte']
    binayList = binayList + nickDict['Jejomar'] + nickDict['Binay']
    poeList = poeList + nickDict['Grace'] + nickDict['Poe']
    roxasList = roxasList + nickDict['Mar'] + nickDict['Roxas']
    santiagoList = santiagoList + nickDict['Miriam'] + nickDict['Defensor'] + nickDict['Santiago']
            
    matrix = []
    final = []
    tempDict = dict()
    rown = 1
    candidate1 = 'Duterte'
    candidate2 = 'Binay'
    candidate3 = 'Poe'
    candidate4 = 'Roxas'
    candidate5 = 'Santiago'
    for i in range(0, 5):
        matrix.append(0)
    for i in range(0, len(tweet_list)):
        tweet = tweet_list[i]
        lower = tweet.lower()
        for i in range(0, 5):
            matrix[i] = 0
        count = lower.split()
        for j in range(0, len(duterteList)): 
            if (duterteList[j].lower() in lower):
                for k in range(0, len(count)):
                    if (duterteList[j].lower() in count[k]):  
                        matrix[0] = k+1
                        break
        for j in range(0, len(binayList)):
            if (binayList[j].lower() in lower):
                for k in range(0, len(count)):
                    if (binayList[j].lower() in count[k]):
                        matrix[1] = k+1
                        break
        for j in range(0, len(poeList)):        
            if (poeList[j].lower() in lower):
                for k in range(0, len(count)):
                    if (poeList[j].lower() in count[k]):
                        matrix[2] = k+1
                        break
        for j in range(0, len(roxasList)):        
            if (roxasList[j].lower() in lower):
                for k in range(0, len(count)):
                    if (roxasList[j].lower() in count[k]):
                        matrix[3] = k+1
                        break
        for j in range(0, len(santiagoList)):        
            if (santiagoList[j].lower() in lower):
                for k in range(0, len(count)):
                    if (santiagoList[j].lower() in count[k]):
                        matrix[4] = k+1
                        break
        tempDict[candidate1] = copy.deepcopy(matrix[0])
        tempDict[candidate2] = copy.deepcopy(matrix[1])
        tempDict[candidate3] = copy.deepcopy(matrix[2])
        tempDict[candidate4] = copy.deepcopy(matrix[3])
        tempDict[candidate5] = copy.deepcopy(matrix[4])
        final.append(copy.deepcopy(tempDict))
        
        print('Tweet Number ' + str(rown) + ' done.')
        rown += 1
            
    knowledgeBase.close()
    return final


