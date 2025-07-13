
import json
import time
from kafka import KafkaProducer
import pandas as pd

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

df = pd.read_csv('../data/gtd.csv')

topic = 'terrorism'

for _, row in df.iterrows():
    message = row.to_dict()
    producer.send(topic, message)
    time.sleep(0.5)  # simulate streaming