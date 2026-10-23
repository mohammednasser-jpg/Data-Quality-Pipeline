import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("--- 🏦 Financial Data Quality & ETL Pipeline ---")
print("1. Generating raw financial transactions...")

# Generate 2000 mock financial transactions
np.random.seed(100)
dates = [datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 30)) for _ in range(2000)]

data = {
    'Transaction_ID': range(50000, 52000),
    'Account_ID': np.random.randint(1000, 1050, 2000),
    'Date': dates,
    'Type': np.random.choice(['Deposit', 'Withdrawal', 'Transfer'], 2000),
    'Amount': np.random.uniform(-500, 5000, 2000) # Intentionally including negative values
}
df = pd.DataFrame(data)

# Injecting bad data for quality checks (Missing Accounts)
df.loc[np.random.choice(df.index, 20, replace=False), 'Account_ID'] = np.nan

print("2. Running Data Quality Checks...")

# Check 1: Flag Missing Account IDs
missing_accounts = df[df['Account_ID'].isna()].copy()
missing_accounts['Error_Reason'] = 'Missing Account ID'

# Check 2: Flag Invalid Amounts (Negative values are not allowed in this system)
invalid_amounts = df[df['Amount'] < 0].copy()
invalid_amounts['Error_Reason'] = 'Negative Transaction Amount'

# Combine all invalid records
invalid_records = pd.concat([missing_accounts, invalid_amounts])

print("3. Segregating Valid and Invalid Data...")

# Filter out the valid records
valid_records = df[~df.index.isin(invalid_records.index)].copy()

# Formatting the valid records
valid_records['Amount'] = valid_records['Amount'].round(2)
valid_records['Date'] = pd.to_datetime(valid_records['Date']).dt.strftime('%Y-%m-%d')
valid_records['Account_ID'] = valid_records['Account_ID'].astype(int)

print("4. Saving outputs...")
valid_records.to_csv('validated_transactions.csv', index=False)
invalid_records.to_csv('flagged_errors.csv', index=False)

print("\n--- Pipeline Summary ---")
print(f"Total Records Processed: {len(df)}")
print(f"✅ Valid Records Saved: {len(valid_records)}")
print(f"⚠️ Flagged Errors (Sent for review): {len(invalid_records)}")
print("Process completed successfully.")