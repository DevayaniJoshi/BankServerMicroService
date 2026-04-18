import os
import pandas as pd
import requests
import zipfile
from config.settings import SERVER_URL
import sys
import time

# default value
TO_PROCESS_RECORDS = 30
TIME_DELAY = 100 #ms
SKIP_ROWS = 0

# override if argument is passed
if len(sys.argv) > 1:
    TO_PROCESS_RECORDS = int(sys.argv[1])

if len(sys.argv) > 2:
    TO_PROCESS_RECORDS = int(sys.argv[1])
    SKIP_ROWS = int(sys.argv[2])

if len(sys.argv) > 3:
    TO_PROCESS_RECORDS = int(sys.argv[1])
    SKIP_ROWS = int(sys.argv[2])
    TIME_DELAY = int(sys.argv[3])

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

csv_path = os.path.join(BASE_DIR, "datasets", "HI-Small_accounts.csv")
zip_path = os.path.join(BASE_DIR, "datasets", "HI-Small_accounts.zip")

url = SERVER_URL + "/api/accounts"

if not os.path.exists(csv_path):
    print("CSV not found. Extracting from ZIP...")

    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(BASE_DIR, "datasets"))
        print("Extraction complete.")
    else:
        raise FileNotFoundError("Neither CSV nor ZIP file found!")

print("\n=== Account Processor Started ===")
print(f"Offset : {SKIP_ROWS}")
print(f"Records to process : {TO_PROCESS_RECORDS}")
print(f"Time delay         : {TIME_DELAY} ms")
print(f"API Endpoint       : {url}")
print(f"CSV Path           : {csv_path}")
print("========================================\n")

df = pd.read_csv(csv_path)
df = df.iloc[SKIP_ROWS: SKIP_ROWS + TO_PROCESS_RECORDS]
count = 0 
for i, row in df.iterrows():
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

    time.sleep(TIME_DELAY / 1000)




 