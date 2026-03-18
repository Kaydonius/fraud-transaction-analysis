# run the pipeline end to end 
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s") 
sys.path.insert(0, os.path.dirname(__file__))


import ingest
import transform




def run():
    project_root = os.path.join(os.path.dirname(__file__), "..")
    data_path = os.path.join(project_root, "data", "raw", "Fraud.csv")
    
    df = ingest.load(data_path)
    ingest.validate(df)

    df = transform.transform(df)
    return df   

if __name__ == "__main__":
    df = run()
    print(df.head())