import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
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
    """
    Writes the data from get_lines() to the database.
    If the same Id exists, it updates the record.
    """
    if not records:
        return
    
    for record in records:
        collection.update_one(
            {"Id": record["Id"]},      
            {"$set": record},          
            upsert=True                 
        )
    print(f"{len(records)} record inserted/updated.")



def update_status(statuses: list):

    """
    Matches the data from get_status() with the records in the DB and updates them.
    - If API LineId = 0, it means no issues on any line.
    - Default: status=False, if matched then status=True.
    """

    if not statuses:
        return
    
    collection.update_many(
        {"status": True},  # Just line was previously marked as having an issue
        {"$set": {
            "status": False,
            "status_description": None,
            "update_date": statuses[0]["UpdateDate"]
        }}
    )

    collection.update_many(
        {},
        {"$set": {"status": False, "status_description": None, "update_date": None}}
    )

    for status in statuses:
        collection.update_one(
            {"Id": status["LineId"]},
            {"$set": {
                "status": True,
                "status_description": status["Description"],
                "update_date": status["UpdateDate"]
            }}
        )
    print(f"{len(statuses)} line status updated., {statuses}")