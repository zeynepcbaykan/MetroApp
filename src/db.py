import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


try:
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
except Exception as e:
    logging.error(f"MongoDB client initialization error: {e}")
    raise e


def connect_db() -> bool:
    """
    Check database connection.
    """
    try:
        client.admin.command('ping')
        logging.info("MongoDB connection successful")
        return True
    except Exception as e:
        logging.error(f"MongoDB connection error: {e}")
        return False

def insert_data(records: list):
    """
    Writes the data from get_lines() to the database.
    If the same Id exists, it updates the record.
    """
    if not records:
        logging.warning("No records to insert/update.")
        return

    inserted_count = 0

    for record in records:
        if "Id" not in record:
            logging.warning(f"Record missing 'Id' field, skipping: {record}")
            continue
        
        record.update({
            "status": False,
            "status_description": None,
            "update_date": None,
            "LineId": None,       
            "Description": None, 
            "Name": record.get("Name")  
        })
        
        try:
            collection.update_many(
                {"Id": record["Id"]},
                {"$set": record},
                upsert=True
            )
            inserted_count += 1
        except Exception as e:
            logging.error(f"Error inserting/updating record {record['Id']}: {e}")
    logging.info(f"{inserted_count}/{len(records)} records inserted/updated.")



def update_status(statuses: list):

    """
    Matches the data from get_status() with the records in the DB and updates them.
    - If API LineId = 0, it means no issues on any line.
    - Default: status=False, if matched then status=True.
    """

    if not statuses:
        logging.warning("No statuses to update.")
        return
    
    try:
        if statuses[0].get("LineId") == 0:
            update_date = statuses[0].get("UpdateDate")
            collection.update_many(
                {"status": True},
                {"$set": {
                    "status": False,
                    "status_description": None,
                    "update_date": update_date
                }}
            )
            logging.info("All line statuses set to False (no issues).")

        updated = 0
        for status in statuses:
            line_id = status.get("LineId")
            if not line_id:
                continue
            try:
                collection.update_one(
                    {"Id": line_id},
                    {"$set": {
                        "status": True,
                        "status_description": status.get("Description"),
                        "update_date": status.get("UpdateDate")
                    }}
                )
                updated += 1
            except Exception as e:
                logging.error(f"Error updating status for LineId {line_id}: {e}")

        logging.info(f"{updated}/{len(statuses)} line statuses updated.")
    except Exception as e:
        logging.error(f"Error in update_status function: {e}")