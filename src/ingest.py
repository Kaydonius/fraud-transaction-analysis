import kagglehub

path = kagglehub.dataset_download("chitwanmanchanda/fraudulent-transactions-data", output_dir="data/raw")

print("Path to dataset files:", path)

