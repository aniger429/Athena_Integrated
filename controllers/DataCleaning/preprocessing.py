import re
from collections import Counter
from DBModels.Username import *


# this function returns a dictionary where the key is the username and the value is the username model class
def create_init_username_df(username_column):
    # All usernames from the column
    frequency = username_column.value_counts()
    u_dict = {}
    for username, freq in frequency.items():
        u_dict['@' + username] = {'numTweets': freq, 'numMentions': 0}

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
    df = data_source[['Tweet', 'Username']]
    username_df = df[['Username']]
    username_df['numTweets'] = df.groupby('Username')['Username'].transform('count')
    username_df['numMentions'] = 0
    username_df.drop_duplicates(keep='first', inplace=True)
    username_df.reset_index(drop=True, inplace=True)

    username_pattern = re.compile("@[a-zA-Z0-9_]+")
    val = list(df.apply(lambda row: re.findall(username_pattern, row['Tweet']), axis=1))
    flat_list = [item for sublist in val for item in sublist]
    ulist = []
    for key, value in Counter(flat_list).items():
        ulist.append({'Username': key[1:], 'numMentions': value, 'numTweets': 0})

    username_df = username_df.append(ulist, ignore_index=True)

    # username_df['length'] = username_df.apply(lambda row: len(row['Username']), axis=1)
    # username_df.drop(df['Username'].str.len() > 17, inplace=True)
    bulk_update(username_df)

    print("Done processing the username")



