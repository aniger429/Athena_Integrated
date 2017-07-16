from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId

db = MongoClient('mongodb://localhost:27017/Athena').Athena


class Username(MongoModel):
    idUsername = fields.IntegerField(primary_key=True)
    username = fields.CharField(max_length=20)
    numTweets = fields.IntegerField(default=False)
    numMentions = fields.IntegerField()
    username_lower = fields.CharField(max_length=20)

    class Meta:
        write_concern = WriteConcern(j=True)


def insert_new_username(username_dict):
    db.Username.insert_many([{'username': key, "numTweets": value['numTweets'], "numMentions": value['numMentions'],
                              "username_lower": key.lower()} for key, value in username_dict.items()])


def bulk_update(username_dict):
    bulk = db.Username.initialize_unordered_bulk_op()
    [bulk.find({'username': key}).upsert().update(
        {
            '$inc': {
                'numTweets': value['numTweets'], 'numMentions': value['numMentions']
            },
            '$set': {'username_lower': key.lower()}
        }
    )for key, value in username_dict.items()]
    bulk.execute()


def get_all_username():
    return db.Username.find()


def get_dict_list_usernames():
    usernames = db.Username.find()
    uNames = []
    idUsername = []
    numMentions = []
    numTweets = []

    for uname in usernames:
        uNames.append(uname['username'])
        numMentions.append(uname['numMentions'])
        numTweets.append(uname['numTweets'])
        idUsername.append('@'+str(uname['_id']))

    unameDict = {'uNames': uNames, 'numMentions': numMentions, 'numTweets': numTweets, 'idUsername': idUsername}

    return unameDict


def get_all_username_tup():
    usernameTup = []
    for user in db.Username.find({}, {'username': 1}):
        usernameTup.append((user['username'], '@'+str(user['_id'])))
    return usernameTup


def get_all_username_dict():
    username_dict = {}
    for user in db.Username.find({}, {'username': 1}):
        username_dict[user['username']] = '@' + str(user['_id'])
    return username_dict


def count_total_usernames():
    return db.Username.count()


def get_all_usernames(num_results):
    return db.Username.find({}, sort=([("numTweets", pymongo.ASCENDING), ("numMentions", pymongo.ASCENDING)]),
                            limit=num_results)


def get_user_data(user_id):
    data = (list(db.Username.find({'_id': ObjectId(user_id)}).limit(1)))
    # data = (list(db.Username.find({'username_lower': '@'+user_id}).limit(1)))
    return data[0]