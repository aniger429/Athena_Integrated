# import peewee
# from peewee import *
#
#
# db = MySQLDatabase('Athena', user='root',passwd='')
#
# class BaseModel(Model):
#     class Meta:
#         database = db
#
# class Username(BaseModel):
#     idUsername = peewee.PrimaryKeyField()
#     username = peewee.CharField()
#     numTweets = peewee.IntegerField()
#     numMentions = peewee.IntegerField()
#
#     class Meta:
#         db_table = "Username"
#         database = db
#
# def insertNewUsername(usernameDict):
#     db.connect()
#
#     # for key, value in usernameDict.items():
#     #     print (key, value.username, value.numMentions, value.numTweets)
#
#     row_dicts = ({'username': key, 'numTweets': value.numTweets, 'numMentions': value.numMentions} for key, value in usernameDict.items())
#     Username.insert_many(row_dicts).execute()
#
#     # for key in usernameCTR:
#     #     userExist, created = Username.create_or_get(username=key, numTweets=usernameCTR[key])
#     #     if created ==  True:
#     #         newNumTweets = userExist.numTweets + usernameCTR[key]
#     #         query = Username.update(numTweets = newNumTweets).where(Username.idUsername  == userExist.idUsername)
#     #         query.execute()
#     db.close()
#
#
# def getAllUsernamesTuple():
#     usernameTup = []
#     for user in Username.select():
#         usernameTup.append((user.username, '@'+str(user.idUsername)))
#     return usernameTup
#
# def getAllUsernamesDict():
#     usernameDict = {}
#     for user in Username.select():
#         usernameDict[user.username] = '@' + str(user.idUsername)
#
#     return usernameDict
#


from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/Athena')
db = client.Athena


class Username(MongoModel):
    idUsername = fields.IntegerField(primary_key=True)
    username = fields.CharField(max_length=20)
    numTweets = fields.IntegerField(default=False)
    numMentions = fields.IntegerField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def insert_new_username(username_dict):
    # row_list = [{'username': key, 'numTweets': value['numTweets'], 'numMentions': value['numMentions']} for key, value
    #             in username_dict.items()]

    row_list = [Username(username=key, numTweets= value['numTweets'], numMentions= value['numMentions']) for key, value in username_dict.items()]

    Username.objects.bulk_create(row_list)


def bulk_update(username_dict):
    bulk = db.username.initialize_ordered_bulk_op()
    [bulk.find({'username': key}).upsert().update(
        {'$set': {'numTweets': value['numTweets'],'numMentions': value['numMentions']}})
     for key, value in username_dict.items()]
    result = bulk.execute()
    print (result)


def get_all_username():
    return db.username.find()


def get_all_username_tup():
    usernameTup = []
    for user in db.username.find({}, {'username': 1}):
        usernameTup.append((user['username'], '@'+str(user['_id'])))
    return usernameTup

def get_all_username_dict():
    username_dict = {}
    for user in db.username.find({}, {'username': 1}):
        username_dict[user['username']] = '@' + str(user['_id'])
    return username_dict


def count_total_usernames():
    return db.username.count()


def get_all_usernames():
    return db.username.find({}).sort([("numTweets",pymongo.ASCENDING), ("numMentions",pymongo.ASCENDING)])


def get_user_data(user_id):
    data = (list(db.username.find({'_id': ObjectId(user_id)}).limit(1)))
    return data[0]