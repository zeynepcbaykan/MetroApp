import os
import logging
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

logging.basicConfig(level=logging.INFO)

def get_client():
    """MongoDB client"""
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
        
        # Eğer LineId=0 ise tüm hatlar normal
        if statuses[0].get("LineId") == 0:
            # update_date null veya 0001-01-01 ise şu anki zamanı kullan
            update_date = statuses[0].get("UpdateDate")
            if not update_date or update_date.startswith("0001-01-01"):
                # Türkiye saati (UTC+3) ve okunabilir format
                update_date = datetime.utcnow().strftime("%d.%m.%Y %H:%M")
            
            result = collection.update_many(
                {},
                {"$set": {
                    "status": False,
                    "status_description": None,
                    "update_date": update_date
                }}
            )
            logging.info(f"All line statuses set to False. {result.modified_count} records updated.")
            return

        # Spesifik hatları güncelle
        updated = 0
        for status in statuses:
            line_id = status.get("LineId")
            if not line_id:
                continue
            
            # update_date null veya 0001-01-01 ise şu anki zamanı kullan
            update_date = status.get("UpdateDate")
            if not update_date or update_date.startswith("0001-01-01"):
                # Türkiye saati (UTC+3) ve okunabilir format
                update_date = datetime.utcnow().strftime("%d.%m.%Y %H:%M")
            
            collection.update_one(
                {"Id": line_id},
                {"$set": {
                    "status": True,
                    "status_description": status.get("Description"),
                    "update_date": update_date
                }}
            )
            updated += 1

        logging.info(f"{updated}/{len(statuses)} line statuses updated.")
    finally:
        if client:
            client.close()
