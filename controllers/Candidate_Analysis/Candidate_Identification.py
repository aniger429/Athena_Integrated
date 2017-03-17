import json
import pandas as pd
import copy
def identify_candidate(tweet_list):
    knowledgeBase = open('C:/Users/HKJ/AppData/Local/Programs/Python/Python35/KB/KnowledgeBase.txt')
    names = json.load(knowledgeBase)

    candidate = []
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
        if (tweet != None):
            lower = tweet.lower()
            for i in range(0, 5):
                matrix[i] = 0
            count = lower.split()
            for j in range(0, len(names[0]["Variations"])): 
                if names[0]["Variations"][j].lower() in lower:
                    for k in range(0, len(count)):
                        if names[0]["Variations"][j].lower() in count[k]:
                            matrix[0] = k+1
                            break
            for j in range(0, len(names[1]["Variations"])):
                if names[1]["Variations"][j].lower() in lower:
                    for k in range(0, len(count)):
                        if names[1]["Variations"][j].lower() in count[k]:
                            matrix[1] = k+1
                            break
            for j in range(0, len(names[2]["Variations"])):        
                if names[2]["Variations"][j].lower() in lower:
                    for k in range(0, len(count)):
                        if names[2]["Variations"][j].lower() in count[k]:
                            matrix[2] = k+1
                            break
            for j in range(0, len(names[3]["Variations"])):        
                if names[3]["Variations"][j].lower() in lower:
                    for k in range(0, len(count)):
                        if names[3]["Variations"][j].lower() in count[k]:
                            matrix[3] = k+1
                            break
            for j in range(0, len(names[4]["Variations"])):        
                if names[4]["Variations"][j].lower() in lower:
                    for k in range(0, len(count)):
                        if names[4]["Variations"][j].lower() in count[k]:
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

