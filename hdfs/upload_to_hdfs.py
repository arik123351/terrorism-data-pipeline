import os
import kagglehub
import subprocess
import glob

# Download GTD dataset
path = kagglehub.dataset_download("START-UMD/gtd")
csv_path = glob.glob(os.path.join(path, "**", "gtd.csv"), recursive=True)[0]

print(f"Uploading {csv_path} to HDFS...")

subprocess.run(["hdfs", "dfs", "-mkdir", "-p", "/datasets/gtd"])
subprocess.run(["hdfs", "dfs", "-put", "-f", csv_path, "/datasets/gtd/"])