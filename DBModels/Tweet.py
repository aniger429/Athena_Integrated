from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
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
    users_mentioned = fields.ListField()

    unigram = fields.ListField()
    bigram = fields.ListField()
    trigram = fields.ListField()


    cand_ana = fields.ListField()


    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def insert_new_tweet(data_to_add):
    db.Tweet.insert_many(data_to_add)


def get_all_tweets():
    client = MongoClient('mongodb://localhost:27017/Athena')
    db = client.Athena

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

def get_everything():
    data = db.Tweet.find({}, {})
    return data


def get_tweets_only():
    result = []
    [result.append(x['tweet']) for x in db.Tweet.find({}, {'_id': 0, 'tweet': 1})]
    return result

# returns all the tweets posted by the user_id
def get_user_tweet_data(user_id):
    data = list(db.Tweet.find({'idUsername': "@"+user_id},{'_id':1,'tweet':1}))
    for d in data:
        d['tweet'] = d['tweet'].split()
    return data

# returns all the tweets a user_id was mentioned
def get_user_mentioned_tweets(user_id):
    data = list(db.Tweet.find({"users_mentioned": {"$in": ["@"+user_id]}},{'_id':1,'tweet':1}))
    for d in data:
        d['tweet'] = d['tweet'].split()
    return data


def get_all_unigrams():
    final = []
    [final.extend(uni['unigram']) for uni in list(db.Tweet.find({},{"unigram":1,"_id":0}))]
    return final


def populate_new_workspace(tweets_dict, db=client.Athena):
    # db.Tweet.insert_many(
    #     [{'idPrimary': t['_id'], "idTweet": t['idTweet'], "idUsername": t['idUsername'],"tweet": t['tweet'],
    #       "date_created": t['date_created'],"hashtags": t['hashtags'],"location": t['location'],
    #       "favorite": t['favorite'],"retweet": t['retweet'],"users_mentioned": t['users_mentioned'],
    #       "unigram": t['unigram'],"bigram": t['bigram'],"trigram": t['trigram'],} for t in
    #      tweets_dict])

    # db.cloneCollection('localhost:27017', 'Athena.Tweet')
    db.cloneCollection('localhost:27017', 'Athena.Tweet',
                       {'active': 'true'})

def into_new_db(tweets, candidate_presence, db=client.Athena):
    print("inserting to db")
    bulk = db.Tweet.initialize_ordered_bulk_op()
    [bulk.find({'_id': key}).upsert().update(
        {'$set': {'cand_ana': value}})
     for key, value in candidate_presence.items()]
    bulk.execute()


def get_candidate_tweets(candidate_name):
    data = list(db.Tweet.find({"cand_ana."+candidate_name: {'$ne': -1}},{'tweet':1, 'cand_ana':1}))
    print (data)
    return data



