import os
import pandas as pd
import requests
from config.settings import SERVER_URL
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

csv_path = os.path.join(BASE_DIR, "datasets", "HI-Small_accounts.csv")
url = SERVER_URL + "/api/accounts"

df = pd.read_csv(csv_path)
TO_PROCESS_RECORDS = 10

count = 0 
for i, row in df.head(TO_PROCESS_RECORDS).iterrows():
    try:
        data = {
            "accountId": row["Account Number"],
            "bankId": str(row["Bank ID"]),
            "entityId": row["Entity ID"],
            "entityName": row["Entity Name"],
            "bankName": row["Bank Name"]
        }

        count = count+1
        response = requests.post(url, json=data)

        if response.status_code >= 300:
            print(f"ERROR: Count: {count} \nResponse Status: {response.status_code} \nResponse Body: {response.json()}")


    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        print(count)





 