import requests
import json

def setup_elasticsearch_index():
    """Set up Elasticsearch index with improved mappings"""
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": "30s"
        },
        "mappings": {
            "properties": {
                "eventid": {"type": "keyword"},
                "iyear": {"type": "integer"},
                "imonth": {"type": "integer"},
                "iday": {"type": "integer"},
                "country_txt": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "region_txt": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "attacktype1_txt": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "nkill": {"type": "integer"},
                "nwound": {"type": "integer"},
                "casualties": {"type": "integer"},
                "timestamp": {"type": "date"},
                "location": {"type": "geo_point"}  # If you have lat/lon data
            }
        }
    }
    
    try:
        # Delete existing index if it exists
        requests.delete('http://localhost:9200/terrorism')
        
        # Create new index
        res = requests.put('http://localhost:9200/terrorism', json=index_settings)
        print(f"Index creation result: {res.json()}")
        return res.status_code == 200
    except Exception as e:
        print(f"Error setting up index: {e}")
        return False