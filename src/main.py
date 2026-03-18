# run the pipeline end to end 
import ingest
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

def run():
    project_root = os.path.join(os.path.dirname(__file__), "..")
    data_path = os.path.join(project_root, "data", "raw", "Fraud.csv")
    
    df = ingest.load("data/raw/Fraud.csv")
    ingest.validate(df)
    return df

if __name__ == "__main__":
    run()