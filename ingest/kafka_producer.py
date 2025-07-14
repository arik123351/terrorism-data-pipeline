import json
import time
import csv
import kafka
import kagglehub
import glob
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_kafka_producer():
    """Create Kafka producer with error handling"""
    try:
        producer = kafka.KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=5,
            batch_size=16384,
            linger_ms=10,
            buffer_memory=33554432
        )
        return producer
    except Exception as e:
        logger.error(f"Failed to create Kafka producer: {e}")
        return None

def send_terrorism_data():
    """Send terrorism data to Kafka with improved error handling"""
    try:
        # Locate the latest GTD dataset
        path = kagglehub.dataset_download("START-UMD/gtd")
        csv_path = glob.glob(os.path.join(path, "**", "gtd.csv"), recursive=True)[0]
        
        producer = create_kafka_producer()
        if not producer:
            return
        
        sent_count = 0
        error_count = 0
        
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Clean and validate data
                    event = {
                        "eventid": row.get("eventid", ""),
                        "iyear": int(row.get("iyear", 0)) if row.get("iyear") else 0,
                        "imonth": int(row.get("imonth", 0)) if row.get("imonth") else 0,
                        "iday": int(row.get("iday", 0)) if row.get("iday") else 0,
                        "country_txt": row.get("country_txt", ""),
                        "region_txt": row.get("region_txt", ""),
                        "attacktype1_txt": row.get("attacktype1_txt", ""),
                        "nkill": int(row.get("nkill", 0)) if row.get("nkill") and row.get("nkill").isdigit() else 0,
                        "nwound": int(row.get("nwound", 0)) if row.get("nwound") and row.get("nwound").isdigit() else 0,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Send to Kafka
                    future = producer.send('terrorism', value=event)
                    future.get(timeout=10)  # Wait for confirmation
                    
                    sent_count += 1
                    if sent_count % 1000 == 0:
                        logger.info(f"Sent {sent_count} events")
                    
                    time.sleep(0.01)  # Reduced sleep time
                    
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error processing row: {e}")
                    
        producer.flush()
        producer.close()
        logger.info(f"Finished sending {sent_count} events with {error_count} errors")
        
    except Exception as e:
        logger.error(f"Error in send_terrorism_data: {e}")