"""FUNCTIONAL REQUIREMENTS
    1. Load raw data
    2. Validate Required Columns
    3. Print/log basic row and column counts"""

import pandas as pd

REQUIRED_COLUMNS = [
    "step", "type", "amount", "nameOrig", "oldbalanceOrg", "newbalanceOrig",
    "nameDest", "oldbalanceDest", "newbalanceDest", "isFraud", "isFlaggedFraud"
]

CORE_COLUMNS = [
    "isFraud", "type", "amount"
]


def load(filepath: str) -> pd.DataFrame:
    # Load raw data
    df = pd.read_csv(filepath)
    print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def validate(df: pd.DataFrame) -> bool:
    # Check if data is empty
    if df.empty:
        raise ValueError("Error: No valid data present")
    else:
        print("Dataset loaded successfully: Checking columns...")

    # Check if required columns exist
    print(f"Validating Data.. Checking if all required columns exist...")
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    else:
        print("No missing columns!\nDuplicate column check...")
    
    # Make sure no duplicate column names
    if df.columns.duplicated().any():
        raise ValueError("Duplicate columns detected.")
    else:
        print("No duplicates!")  

    # Make sure core columns are not completely null
    fully_null = [col for col in CORE_COLUMNS if df[col].isnull().all()]
    if fully_null:
        raise ValueError(f"Core columns fully null: {fully_null}")
    else:
        print("Columns aren't fully null. Checking data types...")
    
    # log row and column counts
    print(f"The data has {df.shape[0]} rows and {df.shape[1]} columns.")
    print("Data validation successful!")
    return True
