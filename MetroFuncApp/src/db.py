import os
import logging
from pymongo import MongoClient
from datetime import datetime, timedelta

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

def get_turkey_time():
    return (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

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
    client = None

    try:
        client = get_client()
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        current_time = get_turkey_time()

        # Önce bütün hatları normal/aktif duruma getir.
        reset_result = collection.update_many(
            {},
            {
                "$set": {
                    "status": False,
                    "status_description": None,
                    "update_date": current_time
                }
            }
        )

        logging.info(
            f"All lines reset to normal. "
            f"{reset_result.modified_count} records modified."
        )

        # API hiç arıza döndürmediyse bütün hatlar normaldir.
        if not statuses:
            logging.info("No service disruptions returned by API.")
            return

        updated = 0

        # API'den dönen hatlar arızalıdır.
        for status in statuses:
            line_id = status.get("LineId")

            # LineId=0 tüm hatların normal olduğunu ifade ediyorsa
            # zaten yukarıda hepsini False yaptık.
            if not line_id:
                continue

            update_date = status.get("UpdateDate")

            if not update_date or update_date.startswith("0001-01-01"):
                update_date = current_time

            result = collection.update_one(
                {"Id": line_id},
                {
                    "$set": {
                        "status": True,
                        "status_description": status.get("Description"),
                        "update_date": update_date
                    }
                }
            )

            logging.info(
                f"LineId={line_id} | "
                f"matched={result.matched_count} | "
                f"modified={result.modified_count} | "
                f"description={status.get('Description')} | "
                f"update_date={update_date}"
            )

            if result.matched_count > 0:
                updated += 1

        logging.info(
            f"{updated}/{len(statuses)} disruption statuses applied."
        )

    finally:
        if client:
            client.close()