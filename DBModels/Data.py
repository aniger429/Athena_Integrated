import datetime

from pymodm import MongoModel, fields
from pymongo import MongoClient
from pymongo.write_concern import WriteConcern

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
    fileCount = db.Data.find({"filename":filename}).count()
    if fileCount == 0:
        return False
    else:
        return True


def insert_new_data(file_name):
    time_uploaded = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    NewFileData = {"filename":file_name, "isClean":"false", "dateUploaded":time_uploaded}
    db.Data.insert_one(NewFileData)


def tweet_cleaned(filename):
    db.Data.update(
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
    return db.Data.find()


def count_total_data():
    return db.Data.count()


def insert_test():
    return db.Tweet.count()
