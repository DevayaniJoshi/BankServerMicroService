import pandas as pd
import requests 
import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
print(script_directory)

# API URL
url = "http://127.0.0.1:8000/api/accounts/"

# CSV load karo
df = pd.read_csv(r"C:\Users\kambl\Desktop\BE Project\BankServerMicroService\Simulation\LI-Small_accounts.csv")
count = 0 

# Column names check (important)
print(df.columns)

# Loop (5 records test ke liye)
for i, row in df.iterrows():
    try:
        data = {
            "accountId": row["Account Number"],
            "bankId": str(row["Bank ID"]),
            "entityId": row["Entity ID"],
            "entityName": row["Entity Name"],
            "bankName": row["Bank Name"]
        }

        print(count+1)
        count = count+1

        response = requests.post(url, json=data)
        if response.status_code >= 300:
            print("Status Code:", response.status_code)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        print(f"Success!")
    finally:
        print("Execution complete.")





 