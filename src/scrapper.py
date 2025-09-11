import requests

BASE_URL = "https://api.ibb.gov.tr/MetroIstanbul/api"

def get_lines():
    response = requests.get(f"{BASE_URL}/MetroMobile/V2//GetLines")
    if response.status_code == 200:
        data = response.json()

        results = [
        {
            "Id": line["Id"],
            "Name": line["Name"],
            "LongDescription": line["LongDescription"],
            "ENDescription": line["ENDescription"],
            "IsActive": line["IsActive"],
        }
        for line in data.get("Data", [])
     ]
        return results
    else:
        print("Failed to fetch lines")
        return []

'''
# Test the function
lines = get_lines()
for line in lines:
    print(line)
'''

def get_status():
    response = requests.get(f"{BASE_URL}/MetroMobile/V2/GetServiceStatuses")
    if response.status_code == 200:
        data = response.json()
        
        results = [
            {
                'Name'  : item['LineName'],
                'LineId': item['LineId'],
                'Description': item['Description'],
                'UpdateDate': item['UpdateDate']
            }
            for item in data.get("Data", [])
        ]
        return results
    else:
        print("Failed to fetch status")
        return []

'''
# Test the function
statuses = get_status()
for status in statuses:
    print(status)
'''