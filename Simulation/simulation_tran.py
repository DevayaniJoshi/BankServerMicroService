import os
import pandas as pd
import requests
import zipfile
from config.settings import SERVER_URL

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

csv_path = os.path.join(BASE_DIR, "datasets", "HI-Small_Trans.csv")
zip_path = os.path.join(BASE_DIR, "datasets", "HI-Small_Trans.zip")

url = SERVER_URL + "/api/transactions"

if not os.path.exists(csv_path):
    print("CSV not found. Extracting from ZIP...")

    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(BASE_DIR, "datasets"))
        print("Extraction complete.")
    else:
        raise FileNotFoundError("Neither CSV nor ZIP file found!")

df = pd.read_csv(csv_path)
TO_PROCESS_RECORDS = 10

count = 0 
for i, row in df.head(TO_PROCESS_RECORDS).iterrows():
    try:
        data = {
            "fromBank": str(row["From Bank"]),
            "fromAccount": str(row["Account"]),
            "toBank": str(row["To Bank"]),
            "toAccount": str(row["Account.1"]),
            "amountReceived": float(row["Amount Received"]),
            "receivingCurrency": row["Receiving Currency"],
            "amountPaid": float(row["Amount Paid"]),
            "paymentCurrency": row["Payment Currency"],
            "paymentFormat": row["Payment Format"]
        }

        count += 1
        response = requests.post(url, json=data)
    
        if response.status_code >= 300:
            print(f"ERROR: Count: {count} \nResponse Status: {response.status_code} \nResponse Body: {response.json()}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        print(count)