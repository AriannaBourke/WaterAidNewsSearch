from pymongo import MongoClient


class Database:
    """ Database class to connect to MongoDB wateraid database """
    client = MongoClient("mongodb://localhost:27017")
    client = MongoClient()
    db = client.wateraid
    reg_users = db.users
    results = db.results
    saved = db.saved
