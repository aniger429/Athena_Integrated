from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
import pandas as pd

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
    return db.Tweet.find()


def get_tweets_only():
    result = []
    [result.append(x['tweet']) for x in db.Tweet.find({}, {'_id': 0, 'tweet': 1})]
    return result

