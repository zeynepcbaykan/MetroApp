import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://api.ibb.gov.tr/MetroIstanbul/api"

def get_lines() -> list[dict]:
    try:
        response = requests.get(f"{BASE_URL}/MetroMobile/V2/GetLines", timeout=10)
        response.raise_for_status()  # HTTP hataları exception olarak fırlatır
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
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = [
            {
                "Name": item.get("LineName"),
                "LineId": item.get("LineId"),
                "Description": item.get("Description"),
                "UpdateDate": item.get("UpdateDate"),
            }
            for item in data.get("Data", [])
            if item.get("LineId") is not None
        ]
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