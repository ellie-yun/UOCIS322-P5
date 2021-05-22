"""
Database insertion and retrieval
"""
from pymongo import MongoClient

class database:
    def __init__(self, db_name="testdb"):
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient('mongodb://' + self.db_name, 27017)
        self.db = self.client.brevetsdb

    def insert(self, row):
        self.db.latestsubmit.insert_one(row)

    def delete_all_rows(self):
        self.db.latestsubmit.delete_many({})

    def list_all_rows(self):
        return list(self.db.latestsubmit.find())
