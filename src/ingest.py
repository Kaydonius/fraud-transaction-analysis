# load raw data and validate


import pandas as pd

# Read data and get basic info
def load_data(file_path):
    df = pd.read_csv(file_path)
    print("Data loaded successfully.")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    return df

# load_data("data/raw/Fraud.csv")

def get_types(df):
    print("Data types:")
    print(df.dtypes)

# get_types(load_data("data/raw/Fraud.csv"))

# validate data - check for missing values, duplicates, etc
def validate_data(df):
    print("Missing values:")
    print(df.isnull().sum())
    print("Duplicate rows:")
    print(df.duplicated().sum())

# validate_data(load_data("data/raw/Fraud.csv"))

# check if target variable is balanced
def check_balance(df, target_col):
    print(f"Value counts for {target_col}:")
    print(df[target_col].value_counts())

check_balance(load_data("data/raw/Fraud.csv"), target_col="isFraud")
