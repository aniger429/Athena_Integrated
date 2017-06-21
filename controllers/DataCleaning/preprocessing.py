import re
from collections import Counter
from DBModels.Username import *


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


def filterOutUsernames(usernameList):
    return [username for username in usernameList if len(username) < 17]


def process_usernames(data_source):
    # 1. Get all usernames from the username columns
    u_dict = create_init_username_df(data_source['Username'])

    tweet_data = data_source['Tweet']
    # 3. Iterate over all Tweet column
    username_pattern = re.compile("@[a-zA-Z0-9_]+")
    found_username_list = []
    [found_username_list.extend(m) for l in tweet_data for m in [username_pattern.findall(l)] if m]
    found_username_list = [username for username in found_username_list if len(username) < 17]

    u_dict = username_mentions(u_dict, found_username_list)

    bulk_update(u_dict)
    # print("Done processing the username")
    return


