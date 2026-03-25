import pandas as pd
import sys

def inspect_csv(file_path):
    try:
        df = pd.read_csv(file_path, nrows=5)
        print(f"--- {file_path} ---")
        print("Columns:", df.columns.tolist())
        print(df.head())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

inspect_csv("HI-Small_accounts.csv")
inspect_csv("HI-Small_Trans.csv")
