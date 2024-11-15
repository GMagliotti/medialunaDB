import os
from pymongo import MongoClient

class MongoConnection:
    def __init__(self, host='localhost', port=27017, database='db'):
        self.client = MongoClient(host, port)
        self.db = self.client[database]

    def set_db(self, db_name):
        self.db = self.client[db_name]
    
    def get_db(self) -> str:
        return self.db

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()

