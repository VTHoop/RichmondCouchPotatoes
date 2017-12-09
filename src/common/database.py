import os

__author__ = 'hooper-p'

import pymongo


class Database(object):
    # URI = "mongodb://127.0.0.1:27017"
    URI = os.environ.get("MONGODB_URI_RCP")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_all(collection):
        return Database.DATABASE[collection].find()

    @staticmethod
    def find_and_sort(collection, query, sortby):
        return Database.DATABASE[collection].find(query).sort(sortby)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, update):
        return Database.DATABASE[collection].update(query, update, upsert=True)

    @staticmethod
    def delete(collection, query):
        return Database.DATABASE[collection].remove(query)

