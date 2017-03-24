import re
from collections import Counter
# from Model.UsernameModel import *
from DBModels.Username import *
import pandas as pd
import time

def findUsername(tweet):
    pattern = '@'


# this function returns a dictionary where the key is the username and the value is the username model class
def create_init_username_df(ulist):
    #All usernames from the column

    u_dict = {}
    for uName, value in dict(Counter(ulist)).items():
        u_dict['@' + uName] = {'numTweets': value, 'numMentions': 0}

    return u_dict


def username_mentions(username_dict, new_username_list):
    # All usernames from the tweets

    for nu, value in dict(Counter(new_username_list)).items():
        if nu not in username_dict:
            username_dict[nu] = {'numTweets': 0, 'numMentions': value}
        else:
            username_dict[nu]['numMentions'] = value
    return username_dict


def addToDB(usernameList):
    insert_new_username(usernameList)
    print("done inserting to table: username")

def filterOutUsernames(usernameList):
    return [username for username in usernameList if len(username) < 17]


def process_usernames(data_source):
    # 1. Get all usernames from the username columns
    u_dict = create_init_username_df(data_source['Username'])

    tweet_data = data_source['Tweet']
    # 3. Iterate over all Tweet column
    pattern = re.compile("@[a-zA-Z0-9_]+")
    found_username_list = []
    [found_username_list.extend(m) for l in tweet_data for m in [pattern.findall(l)] if m]
    found_username_list = filterOutUsernames(found_username_list)

    u_dict = username_mentions(u_dict, found_username_list)

    addToDB(u_dict)
    print("Done processing the username")
    return 0


def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8')


# from pymodm import connect
# # Connect to MongoDB and call the connection "athenaDB.
# connect("mongodb://localhost:27017/Athena", alias="athenaDB")
#
#
# start = time.time()
# file_name = "C:\\Users\\Regina\\Google Drive\\Thesis\\Dummy Data\\test1.xlsx"
# process_usernames(read_xlsx(file_name))
#
# ulist = get_all_username()
#
# ctr = 1
# for u in ulist:
#     print(str(ctr) + " : " + str(u['_id']) + " : " + u['username'])
#     ctr = ctr + 1
#
# end = time.time()
# print("Time to clean file:" + str(end - start))
#

