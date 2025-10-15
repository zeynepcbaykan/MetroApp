import requests
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://api.ibb.gov.tr/MetroIstanbul/api"

def get_lines() -> list[dict]:
    try:
        response = requests.get(f"{BASE_URL}/MetroMobile/V2/GetLines")
        response.raise_for_status()
        data = response.json()

        results = [
            {
                "Id": line.get("Id"),
                "Name": line.get("Name"),
                "LongDescription": line.get("LongDescription"),
                "ENDescription": line.get("ENDescription"),
                "IsActive": line.get("IsActive", False),
            }
            for line in data.get("Data", [])
            if line.get("Id") is not None
        ]
        logging.info(f"{len(results)} lines fetched successfully.")
        return results

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch lines: {e}")
        return []
    except ValueError as e:
        logging.error(f"Error parsing JSON for lines: {e}")
        return []

'''
# Test the function
lines = get_lines()
for line in lines:
    print(line)
'''

def get_status():
    try:
        response = requests.get(f"{BASE_URL}/MetroMobile/V2/GetServiceStatuses")
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("Data", []):
            if item.get("LineId") is None:
                continue
            
            # UpdateDate kontrol et - eğer 0001-01-01 ise okunabilir formatta şu anki zamanı kullan
            update_date = item.get("UpdateDate")
            if not update_date or update_date.startswith("0001-01-01"):
                update_date = datetime.utcnow().strftime("%d.%m.%Y %H:%M")  # ✅ Okunabilir format
            
            results.append({
                "Name": item.get("LineName"),
                "LineId": item.get("LineId"),
                "Description": item.get("Description"),
                "UpdateDate": update_date
            })
        
        logging.info(f"{len(results)} line statuses fetched successfully.")
        return results

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch statuses: {e}")
        return []
    except ValueError as e:
        logging.error(f"Error parsing JSON for statuses: {e}")
        return []


'''
# Test the function
statuses = get_status()
for status in statuses:
    print(status)
'''