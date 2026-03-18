import pandas as pd
import logging

logger = logging.getLogger(__name__)

# clean column names
def clean_column_names(df):
    # remove whitespace, lowercase, spaces, and special characters
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
                  .str.replace("[()$]", "", regex=True))
    return df

# check/handle missing values
def check_missing_values(df):
    # check for missing values and print counts
    logger.info(f"Missing values in each column:\n{df.isna().sum()}")
    # no missing values, so no imputation needed
    return df
    
# parse timestamps
def parse_timestamps(df):
    # convert step to datetime, 1 step = 1 hour
    df["timestamp"] = pd.to_datetime(df["step"], unit="h", origin="2020-01-01")
    return df

# remove duplicates/unecessary columns if needed
def remove_duplicates(df):
    # check for duplicates
    if df.duplicated().any():
        logger.info(f"Found {df.duplicated().sum()} duplicate rows. Removing them...")
        df = df.drop_duplicates()
    else:
        logger.info("No duplicate rows found.")
    return df


# output new dataframe
def transform(df):
    df = clean_column_names(df)
    df = check_missing_values(df)
    df = parse_timestamps(df)
    df = remove_duplicates(df)
    return df
