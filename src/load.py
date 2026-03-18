# make sqlite database and load clean data into it
import sqlite3
import logging
import pandas as pd
import os

logger = logging.getLogger(__name__)

# define file path and table name
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "transactions.db")
TABLE_NAME = "transaction_data"

# connect to sqlite DB
def connect_to_db(database_path: str=DB_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    logger.info("Database created and connected successfully.")
    return connection


# load clean data into database
def load_data(df: pd.DataFrame, connection: sqlite3.Connection):
    # initializes schema from the dataframe directly
    df.to_sql(TABLE_NAME, connection, if_exists='replace', index=False)
    logger.info(f"Loaded {len(df)} rows into '{TABLE_NAME}'.")

# run it
def run(df: pd.DataFrame):
    connection = connect_to_db()
    load_data(df, connection)
    connection.close()
    logger.info(f"Database load complete")
