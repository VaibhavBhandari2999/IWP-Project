import pymongo
__author__='Vaibhav'

class Database:
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['office_test_1']

    @staticmethod
    def insert(collection,data):
        #print(collection,data)
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection,query):
        return Database.DATABASE[collection].find_one(query)
        #return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_collection(collection):
        return Database.DATABASE[collection].find()

    @staticmethod
    def update(collection,query,data):
        Database.DATABASE[collection].update(query,data,upsert=True)

    @staticmethod
    def delete(collection,query):
        Database.DATABASE[collection].remove(query)

    @staticmethod
    def count_documents(collection,query):
        return Database.DATABASE[collection].count(query)