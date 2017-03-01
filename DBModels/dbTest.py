# from flask import Flask
# from flask_mongoalchemy import MongoAlchemy
# app = Flask(__name__)
# app.config['MONGOALCHEMY_DATABASE'] = 'Athena'
# db = MongoAlchemy(app)
#
# class Tweets(db.Document):
#     name = db.StringField()
#
# class Book(db.Document):
#     title = db.StringField()
#     author = db.DocumentField(Author)
#     year = db.IntField()
#
#
# mark_pilgrim = Author(name='Mark Pilgrim')
# dive = Book(title='Dive Into Python', author=mark_pilgrim, year=2004)
# mark_pilgrim.save()
# dive.save()


from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
import datetime


class Data(MongoModel):
    idData = fields.IntegerField(primary_key=True, min_value=1)
    filename = fields.CharField(max_length=255)
    isClean = fields.BooleanField(default=False)
    dateUploaded = fields.DateTimeField()
    # tweetStartID = fields.IntegerField()
    # tweetEndID = fields.IntegerField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'athenaDB'


def insert_new_data(file_name):
    time_uploaded = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    Data(filename=file_name, dateUploaded=time_uploaded).save()


def get_all_file():
    for user in Data.objects.all():
        print(user.filename + ' ' + str(user.isClean) + ' ' + str(user.dateUploaded))

    return Data.objects.all()