import pandas as pd
import requests

# URL (important)
url = "http://127.0.0.1:8000/transactions/"

# CSV load
df = pd.read_csv(r"C:\Users\kambl\Desktop\BE Project\BankServerMicroService\Simulation\LI-Small_Trans.csv")

# Columns check
print(df.columns)

count = 0

# First 10 records test
for i, row in df.head(10).iterrows():
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
        print(f"Sending Transaction {count}")

        response = requests.post(url, json=data)

        # Debug response
        print("Status:", response.status_code)
        print("Response:", response.text)

        if response.status_code < 300:
            print("Success ✅")
        else:
            print("Error ❌")

    except Exception as e:
        print("Exception:", e)

    finally:
        print("Done\n")