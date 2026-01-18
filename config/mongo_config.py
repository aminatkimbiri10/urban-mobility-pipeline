# config/mongo_config.py

from pymongo import MongoClient

MONGO_URI = (
    "mongodb+srv://aminatakimbiri:aminatakimbiri25@cluster0.tgepib5.mongodb.net/"
)

DATABASE_NAME = "urban_mobility"

def get_mongo_client():
    return MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=20000,
        socketTimeoutMS=20000,
    )

def get_database():
    client = get_mongo_client()
    return client[DATABASE_NAME]
