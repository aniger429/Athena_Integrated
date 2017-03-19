
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/Athena')
db = client.Athena


class KBFile(MongoModel):
    idKBFile = fields.IntegerField(primary_key=True)
    filename = fields.CharField(max_length=255)
    dateUploaded = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def check_if_kbfile_exists(filename):
    fileCount = db.kbfile.find({"filename":filename}).count()
    if fileCount == 0:
        return False
    else:
        return True

def insert_new_kbfile(file_name):
    time_uploaded = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    KBFile(filename=file_name, dateUploaded=time_uploaded).save()


def get_all_kbfile():
    data = list(db.kb_file.find())
    return data


def count_total_kbfile():
    return db.kbfile.count()
