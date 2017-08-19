from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/Athena')
db = client.Athena


def restart_database_mongo():
    client.drop_database("Athena")
    return
