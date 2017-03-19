
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/Athena')
db = client.Athena


class KB_Names(MongoModel):
    id = fields.IntegerField(primary_key=True)
    candidate_name = fields.CharField()
    kb_names = fields.ListField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def insert_new_kb_names(kb_names_dict):
    row_list = [KB_Names(candidate_name=key, kb_names=value) for
                key, value in kb_names_dict.items()]
    KB_Names.objects.bulk_create(row_list)


def get_all_kb_names():
    data = list(db.kb__names.find({},{"_id":0, "_cls":0}))
    return data


def count_total_candidate():
    return db.kb__names.find({}).count()

