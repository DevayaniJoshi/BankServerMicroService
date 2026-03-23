import pandas as pd
import requests

# API URL
url = "http://127.0.0.1:8000/api/accounts/"

# CSV load karo
df = pd.read_csv(r"C:\Users\kambl\Desktop\BE Project\BankServerMicroService\Simulation\LI-Small_accounts.csv")


# Column names check (important)
print(df.columns)

# Loop (5 records test ke liye)
for i, row in df.head(5).iterrows():

    data = {
        "accountId": row["Account Number"],
        "bankId": row["Bank ID"],
        "entityId": row["Entity ID"],
        "entityName": row["Entity Name"],
        "bankName": row["Bank Name"]
    }

    print(data)

    response = requests.post(url, json=data)

    print("Status Code:", response.status_code)
    





 