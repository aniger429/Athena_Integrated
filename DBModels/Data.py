# import peewee
# from peewee import *
# import datetime
#
# db = MySQLDatabase('Athena', user='root', passwd='')
#
# class BaseModel(Model):
#     class Meta:
#         database = db
#
# class Data(BaseModel):
#     idData = peewee.PrimaryKeyField()
#     filename = peewee.CharField(max_length=255, null=False)
#     isClean = peewee.BooleanField(default=False, null=False)
#     dateCreated = peewee.DateTimeField(default=datetime.datetime.now, null=False)
#     tweetStartID = peewee.IntegerField(default=0, null=True)
#     tweetEndID = peewee.IntegerField(default=0, null=True)
#
#     class Meta:
#         db_table = "Data"
#         database = db
#
# def insertNewData(filename):
#     db.connect()
#     Data.insert(filename=filename).execute()
#     db.close()
#
# def tweet_cleaned(filename):
#     db.connect()
#     Data.update(isClean=1).where(filename == filename).execute()
#     db.close()
#
#
# def getAllData():
#     return Data.select()

from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/Athena')
db = client.Athena


class Data(MongoModel):
    idData = fields.IntegerField(primary_key=True)
    filename = fields.CharField(max_length=255)
    isClean = fields.BooleanField(default=False)
    dateUploaded = fields.DateTimeField()
    # tweetStartID = fields.IntegerField()
    # tweetEndID = fields.IntegerField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def check_if_file_exists(filename):
    fileCount = db.data.find({"filename":filename}).count()
    if fileCount == 0:
        return False
    else:
        return True

def insert_new_data(file_name):
    time_uploaded = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    Data(filename=file_name, dateUploaded=time_uploaded).save()


def tweet_cleaned(filename):
    db.data.update(
        {'filename': filename},
        {'$set':
            {
                'isClean': 'true',
            }
        }
    )

def get_all_file():
    # for user in db.data.find():
    #     print(user['filename'])
    return db.data.find()


def count_total_data():
    return db.data.count()
