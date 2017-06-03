import re
from collections import Counter
import pandas as pd
from Model.UsernameModel import *
from DBModels.Username import *


def readXLSX(filename):
    return pd.read_excel(filename)

def findUsername(tweet):
    pattern = '@'

#this function returns a dictionary where the key is the username and the value is the username model class
def createInitUsernameList(usernameList):
    #All usernames from the column
    usernameDict = {}

    for u, value in dict(Counter(usernameList)).items():
        user = UsernameModel(username = '@'+u, numTweets=value)
        usernameDict['@'+u] = user
    return usernameDict

def usernameMentions(usernameDict, newUsernameList):
    # All usernames from the tweets

    for nu, value in dict(Counter(newUsernameList)).items():
        if nu not in usernameDict:
            user = UsernameModel(username = nu, numMentions=value)
            usernameDict[nu] = user
        else:
            usernameDict[nu].numMentions = value
    return usernameDict


def addToDB(usernameList):
    insertNewUsername(usernameList)
    print ("done inserting to table: username")

def filterOutUsernames(usernameList):
    return  [username for username in usernameList if len(username) < 17]


def processUsernames(file_name):
    data = readXLSX(file_name)

    # 1. Get all usernames from the username columns
    usernameDict = createInitUsernameList(data['Username'])

    Tweets = data['Tweet']
    # 3. Iterate over all Tweet column
    pattern = re.compile("@[a-zA-Z0-9_]+")
    foundUsernameList = []
    [foundUsernameList.extend(m) for l in Tweets for m in [pattern.findall(l)] if m]
    foundUsernameList = filterOutUsernames(foundUsernameList)
    usernameDict = usernameMentions(usernameDict, foundUsernameList)

    addToDB(usernameDict)


file_name = "C:/Users/HKJ/AppData/Local/Programs/Python/Python35/Data Cleaning//Election-18.xlsx"
usernameIDs = getAllUsernames()
print (usernameIDs)

