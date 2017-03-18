from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
import pandas as pd
from bson.objectid import ObjectId


from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/Athena')
db = client.Athena


class Tweet(MongoModel):
    idPrimary = fields.BigIntegerField(primary_key=True)
    idTweet = fields.CharField()
    idUsername = fields.CharField()
    tweet = fields.CharField()
    date_created = fields.DateTimeField()
    hashtags = fields.ListField()
    location = fields.CharField()
    favorite = fields.IntegerField()
    retweet = fields.IntegerField()

    unigram = fields.ListField()
    bigram = fields.ListField()
    trigram = fields.ListField()


    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def insert_new_tweet(data_to_add):
    for t in data_to_add:
        print(t['tweet'])
    db.Tweet.insert_many(data_to_add)


def get_all_tweets():
    data = list(db.Tweet.find({},{'_id':1,'tweet':1}))

    for d in data:
        d['tweet'] = d['tweet'].split()

    return data


def count_total_tweet():
    return db.Tweet.count()


def get_tweet_data(tweet_id):
    data = (list(db.Tweet.find({'_id':ObjectId(tweet_id)}).limit(1)))
    data[0]['tweet'] = data[0]['tweet'].split()
    return data[0]


def get_tweets_only():
    result = []
    [result.append(x['tweet']) for x in db.Tweet.find({}, {'_id': 0, 'tweet': 1})]
    return result

def get_user_tweet_data(user_id):
    data = db.Tweet.find({'idUsername': "@"+user_id},{'_id':1,'tweet':1})
    return data
