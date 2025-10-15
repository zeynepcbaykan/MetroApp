import os
from pymongo import MongoClient
import requests

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

response = requests.get("https://api.ibb.gov.tr/MetroIstanbul/api/MetroMobile/V2/GetLines")
lines = response.json()["Data"]

for line in lines:
    collection.update_one(
        {"Id": line["Id"]},
        {"$set": {
            "Id": line["Id"],
            "Name": line["Name"],
            "LongDescription": line.get("LongDescription"),
            "ENDescription": line.get("ENDescription"),
            "IsActive": line.get("IsActive", False),
            "status": False,
            "status_description": None,
            "update_date": None,
            "LineId": None,
            "Description": None
        }},
        upsert=True
    )

print(f"✅ {len(lines)} metro hattı Cosmos DB'ye yüklendi!")
client.close()