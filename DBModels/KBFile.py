import datetime

from pymodm import MongoModel, fields
from pymongo import MongoClient
from pymongo.write_concern import WriteConcern

client = MongoClient('mongodb://localhost:27017/Athena')
db = client.Athena


class KB_File(MongoModel):
    idKBFile = fields.IntegerField(primary_key=True)
    filename = fields.CharField(max_length=255)
    dateUploaded = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def check_if_kbfile_exists(filename):
    fileCount = db.KB_File.find({"filename": filename}).count()
    if fileCount == 0:
        return False
    else:
        return True


def insert_new_kbfile(file_name):
    time_uploaded = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    NewFileData = {"filename": file_name, "dateUploaded": time_uploaded}
    db.KB_File.insert_one(NewFileData)


def get_all_kbfile():
    data = list(db.KB_File.find())
    return data


def count_total_kbfile():
    return db.KB_File.count()
