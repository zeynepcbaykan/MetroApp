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
    """
    get_lines() datasını DB'ye yazar.
    Eğer aynı Id varsa update eder.
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
    get_status() datasını DB'deki kayıtlarla eşleştirip günceller.
    Varsayılan: status=False, eşleşirse status=True.
    """
    if statuses is None:
        return
    
    collection.update_many(
        {},
        {"$set": {"status": False, "status_description": None, "update_date": None}}
    )

    # gelen statusleri işliyoruz
    for status in statuses:
        collection.update_one(
            {"Id": status["LineId"]},  # LineId ↔ Id eşleşmesi
            {"$set": {
                "status": True,
                "status_description": status["Description"],
                "update_date": status["UpdateDate"]
            }}
        )
    print(f"{len(statuses)} line status updated.")