import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "metro_ariza")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "arizalar")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


def connect_db():
    """
    Check database connection.
    """
    try:
        client.admin.command('ping')
        print("MongoDB connection successful")
        return True
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return False


def insert_data(records: list):
    pass


def update_column():
    pass