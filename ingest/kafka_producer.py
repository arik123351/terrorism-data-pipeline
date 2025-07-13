import json
import time
import csv
import kafka
import kagglehub
import glob
import os

# Locate the latest GTD dataset
path = kagglehub.dataset_download("START-UMD/gtd")
csv_path = glob.glob(os.path.join(path, "**", "gtd.csv"), recursive=True)[0]

producer = kafka.KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        event = {
            "eventid": row["eventid"],
            "iyear": int(row["iyear"]),
            "imonth": int(row["imonth"]),
            "iday": int(row["iday"]),
            "country_txt": row["country_txt"],
            "region_txt": row["region_txt"],
            "attacktype1_txt": row["attacktype1_txt"],
            "nkill": int(row["nkill"]) if row["nkill"] else 0,
            "nwound": int(row["nwound"]) if row["nwound"] else 0
        }
        producer.send('terrorism', value=event)
        time.sleep(0.1)