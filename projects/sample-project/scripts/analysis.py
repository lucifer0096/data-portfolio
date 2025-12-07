# Simple analysis script for Sample Sales EDA
# Rahul Bhaskaran

import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_sales.csv"

def main():
    df = pd.read_csv(DATA_PATH)
    print("Sample of data:")
    print(df.head().to_string(index=False))
    print("\nSummary statistics:")
    print(df.describe(include='all').to_string())

    # Example aggregation
    if 'date' in df.columns and 'sales' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        monthly = df.resample('M', on='date')['sales'].sum().reset_index()
        print("\nMonthly sales:")
        print(monthly.to_string(index=False))

if __name__ == "__main__":
    main()
