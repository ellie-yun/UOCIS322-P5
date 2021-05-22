"""
Database insertion and retrieval
"""
from pymongo import MongoClient

class Mongodb:
    def __init__(self, client_name="testclient"):
        self.client_name = client_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient('mongodb://' + self.client_name, 27017)

    def set_db(self, db_name):
        self.db = self.client[db_name]

    def insert(self, collection, row):
        self.db[collection].insert_one(row)

    def delete_all_rows(self, collection):
        self.db[collection].delete_many({})

    def list_all_rows(self, collection):
        return list(self.db[collection].find())


