import pymongo
import certifi
from flask import g


def connect_db(mongo_uri: str):
    client = pymongo.MongoClient(mongo_uri, tlsCAFile=certifi.where())
    client.admin.command("ping")
    g.mongo_client = client
    return None


def close_db_connection():
    db = g.pop("mongo_client", None)
    if db:
        print("Closing Database connection")
        db.close()
    return None
