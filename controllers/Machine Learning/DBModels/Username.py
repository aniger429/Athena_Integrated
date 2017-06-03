import peewee
from peewee import *


db = MySQLDatabase('Athena', user='root',passwd='')

class BaseModel(Model):
    class Meta:
        database = db

class Username(BaseModel):
    idUsername = peewee.PrimaryKeyField()
    username = peewee.CharField()
    numTweets = peewee.IntegerField()
    numMentions = peewee.IntegerField()

    class Meta:
        db_table = "Username"
        database = db

def insertNewUsername(usernameDict):
    db.connect()

    # for key, value in usernameDict.items():
    #     print (key, value.username, value.numMentions, value.numTweets)

    row_dicts = ({'username': key, 'numTweets': value.numTweets, 'numMentions': value.numMentions} for key, value in usernameDict.items())
    Username.insert_many(row_dicts).execute()

    # for key in usernameCTR:
    #     userExist, created = Username.create_or_get(username=key, numTweets=usernameCTR[key])
    #     if created ==  True:
    #         newNumTweets = userExist.numTweets + usernameCTR[key]
    #         query = Username.update(numTweets = newNumTweets).where(Username.idUsername  == userExist.idUsername)
    #         query.execute()
    db.close()


def getAllUsernames():
    usernameTup = []
    for user in Username.select():
        usernameTup.append((user.username, '@'+str(user.idUsername)))

    return usernameTup
