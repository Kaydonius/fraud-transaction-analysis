"""FUNCTIONAL REQUIREMENTS
    1. Load Raw Data
    2. Validate Required Columns
    3. Print/log basic row and column counts"""

import pandas as pd

def load(data):
    # read in data
    df = pd.read_csv(data)
    res = df.dtypes

    series_valid = {
        'step': 'int64',
        'type': 'str',
        'amount': 'float64',
        'nameOrig': 'str',
        'oldbalanceOrg': 'float64',
        'newbalanceOrig': 'float64',
        'nameDest': 'str',
        'oldbalanceDest': 'float64',
        'newbalanceDest': 'float64', 
        'isFraud': 'int64',
        'isFlaggedFraud': 'int64'
    }
  
    # column check/validation
    col_check = []

    if df.empty:
        print("Error: No valid data present")
    else:
        print("Dataset loaded successfully: Checking columns...")

        for cols in df.columns:
            col_check.append(cols)

        required_columns = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig',
                            'nameDest', 'oldbalanceDest', 'newbalanceDest', 'isFraud', 'isFlaggedFraud']
        
        if required_columns == col_check:
            print("Required columns passed!")
        else:
            print("Error: Missing Data")
            print(col_check)
            print(required_columns)

        print("Checking for and removing duplicated rows...")
        if df.duplicated().any():
            df.drop_duplicates()
        else:
            print("No columns dropped!")

        print("Checking null values...")
        if df.isnull:
            print(f"Amount of null values in each column:\n{df.isnull().sum()}")

        print("Checking data types...")
        if res.any() == series_valid:
            print("All data types match!")
        else:
            mismatched_columns = []
            for cols, series_valid in series_valid.items():
                if cols in res.index:
                    if str(res[cols] != series_valid):
                        mismatched_columns.append({
                            "Column": cols,
                            "Actual Dtype": str(res[cols]),
                            "Expected Dtype": series_valid
                        })
            print("Data types don't match:\n")
            for mismatch in mismatched_columns:
                print(f"Column: {mismatch['Column']}, Actual: {mismatch['Actual Dtype']}, Expected: {mismatch['Expected Dtype']}")
            

    print("\nData validation successful!")
