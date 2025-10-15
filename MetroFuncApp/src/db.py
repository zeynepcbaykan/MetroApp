import os
import logging
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

logging.basicConfig(level=logging.INFO)

def get_client():
    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=30000
        )
        return client
    except Exception as e:
        logging.error(f"MongoDB client error: {e}")
        raise

def connect_db() -> bool:
    try:
        client = get_client()
        client.admin.command('ping')
        logging.info("MongoDB connection successful")
        client.close()
        return True
    except Exception as e:
        logging.error(f"MongoDB connection error: {e}")
        return False

def insert_data(records: list):
    if not records:
        return
    
    client = None
    try:
        client = get_client()
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        inserted = 0
        for record in records:
            if "Id" not in record:
                continue
            
            record.update({
                "status": False,
                "status_description": None,
                "update_date": None,
                "LineId": None,
                "Description": None,
                "Name": record.get("Name")
            })
            
            collection.update_one(
                {"Id": record["Id"]},
                {"$set": record},
                upsert=True
            )
            inserted += 1
        
        logging.info(f"{inserted}/{len(records)} records inserted/updated.")
    finally:
        if client:
            client.close()

def update_status(statuses: list):
    if not statuses:
        return
    
    client = None
    try:
        client = get_client()
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        if statuses[0].get("LineId") == 0:
            collection.update_many(
                {"status": True},
                {"$set": {
                    "status": False,
                    "status_description": None,
                    "update_date": statuses[0].get("UpdateDate")
                }}
            )
            logging.info("All line statuses set to False.")

        updated = 0
        for status in statuses:
            line_id = status.get("LineId")
            if not line_id:
                continue
            
            collection.update_one(
                {"Id": line_id},
                {"$set": {
                    "status": True,
                    "status_description": status.get("Description"),
                    "update_date": status.get("UpdateDate")
                }}
            )
            updated += 1

        logging.info(f"{updated}/{len(statuses)} line statuses updated.")
    finally:
        if client:
            client.close()
