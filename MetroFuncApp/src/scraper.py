import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://api.ibb.gov.tr/MetroIstanbul/api"

def get_turkey_time():
    """Türkiye saati (UTC+3)"""
    return (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

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

def get_status():
    try:
        response = requests.get(f"{BASE_URL}/MetroMobile/V2/GetServiceStatuses")
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("Data", []):
            if item.get("LineId") is None:
                continue
            
            # UpdateDate kontrol et - eğer 0001-01-01 ise Türkiye saatini kullan
            update_date = item.get("UpdateDate")
            if not update_date or update_date.startswith("0001-01-01"):
                update_date = get_turkey_time() 
            
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