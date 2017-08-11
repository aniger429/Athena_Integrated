from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from pymongo import MongoClient
import pandas as pd

client = MongoClient('mongodb://localhost:27017/Athena')
db = client.Athena


class Lexicon(MongoModel):
    id = fields.IntegerField(primary_key=True)
    language = fields.CharField()
    sentiment = fields.CharField()
    words = fields.ListField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def insert_lexicon_sentiments(language, positive, negative):
    db.Lexicon.insert_one({'language': language, "sentiment": "positive", "words": positive})
    db.Lexicon.insert_one({'language': language, "sentiment": "negative", "words": negative})


def get_all_lexicon():
    data = pd.DataFrame(list(db.Lexicon.find({}, {"_id": 0, "_cls": 0})))
    print(data)
    return data


# returns all the words of the lexicons for a language and sentiment
def get_all_words(language, sentiment):
    data = db.Lexicon.find_one({'language': language, 'sentiment': sentiment}, {"sentiment": 0, "language": 0, "_id": 0, "_cls": 0})
    return data['words']


# add new names for candidate
def new_lexicon_words(names, language, sentiment):
    return db.Lexicon.update({'language': language, 'sentiment': sentiment}, {"$pushAll": {'words': names}})


# # deletes all candidate names in the list
def delete_lexicon_words(names, language, sentiment):
    return db.Lexicon.update({'language': language, 'sentiment': sentiment}, {'$pullAll': {'words': names}})




