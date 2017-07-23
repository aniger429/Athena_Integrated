from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/Athena')
db = client.Athena


class KB_Names(MongoModel):
    id = fields.IntegerField(primary_key=True)
    candidate_name = fields.CharField()
    kb_names = fields.ListField()
    blacklist_names = fields.ListField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def insert_new_kb_names(kb_names_dict):
    db.KB_Names.insert_many(
        [{'candidate_name': key, "kb_names": value, "blacklist_names": []} for key, value in
         kb_names_dict.items()])


def kb_names_update(kb_names_dict):
    bulk = db.KB_Names.initialize_ordered_bulk_op()

    [bulk.find({'candidate_name': key}).update_one(
        {'$addToSet': { 'kb_names': {'$each': value }}})
     for key, value in kb_names_dict.items()]

    result = bulk.execute()


def get_all_kb_names():
    data = list(db.KB_Names.find({},{"_id":0, "_cls":0}))
    return data


def count_total_candidate():
    return db.KB_Names.find({}).count()


def get_specific_candidate_names(cname):
    data = list(db.KB_Names.find({'candidate_name':cname}, {"_id": 0, "_cls": 0}))
    return data[0]


# returns all the names of the candidates in the db
def get_all_candidate_names():
    return list(db.KB_Names.distinct("candidate_name"))


# add new names for candidate
def new_kb_names(names, candidate):
    return db.KB_Names.update({"candidate_name": candidate}, {"$pushAll": {'kb_names': names}})


# deletes all candidate names in the list
def delete_kb_names(names, candidate):
    db.KB_Names.update({"candidate_name": candidate}, {"$pushAll": {'blacklist_names': names}})

    return db.KB_Names.update({'candidate_name': candidate},
                                               {'$pullAll': {'kb_names': names}})

