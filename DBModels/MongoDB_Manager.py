import datetime

from pymodm import MongoModel, fields
from pymongo import MongoClient
from pymongo.write_concern import WriteConcern

mainDB = "Athena"
client = MongoClient('localhost', 27017)
db = client[mainDB]

class Workspace(MongoModel):
    idWorkspace = fields.IntegerField(primary_key=True)
    name = fields.CharField(max_length=255)
    date_created = fields.DateTimeField()


    class Meta:
        write_concern = WriteConcern(j=True)
        # connection_alias = 'athenaDB'


def check_if_workspace_exists(name):
    fileCount = db.Workspace.find({"name":name}).count()
    if fileCount == 0:
        return False
    else:
        return True


def create_new_workspace(name):
    if(check_if_workspace_exists(name) == False):
        time_uploaded = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        NewFileData = {"name": name, "date_created": time_uploaded}
        db.Workspace.insert_one(NewFileData)


def get_all_workspace():
    return db.Workspace.find()


def count_total_workspace():
    return db.Workspace.count()


def get_db_instance(db_name):
    return client[db_name]
