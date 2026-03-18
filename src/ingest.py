import pandas as pd
import logging

logger = logging.getLogger(__name__)

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
    logger.info(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def validate(df: pd.DataFrame) -> bool:
    # Check if data is empty
    if df.empty:
        raise ValueError("Error: No valid data present")
    else:
        logger.info("Dataset loaded successfully: Checking columns...")

    # Check if required columns exist
    logger.info(f"Validating Data.. Checking if all required columns exist...")
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    else:
        logger.info("No missing columns. Duplicate column check...")
    
    # Make sure no duplicate column names
    if df.columns.duplicated().any():
        raise ValueError("Duplicate columns detected.")
    else:
        logger.info("No duplicates!")  

    # Make sure core columns are not completely null
    fully_null = [col for col in CORE_COLUMNS if df[col].isnull().all()]
    if fully_null:
        raise ValueError(f"Core columns fully null: {fully_null}")
    else:
        logger.info("Columns aren't fully null.")
    
    # log row and column counts
    logger.info(f"The data has {df.shape[0]} rows and {df.shape[1]} columns.")
    logger.info("Data validation successful!")
    return True
