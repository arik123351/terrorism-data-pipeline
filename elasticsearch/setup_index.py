import requests
import json
import time
from requests.exceptions import ConnectionError, Timeout

def check_elasticsearch_connection(host='localhost', port=9200, timeout=5):
    """Check if Elasticsearch is running and accessible"""
    try:
        response = requests.get(f'http://{host}:{port}', timeout=timeout)
        return response.status_code == 200
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def setup_elasticsearch_index(host='localhost', port=9200, index_name='terrorism'):
    """Set up Elasticsearch index with improved mappings and error handling"""
    
    # First check if Elasticsearch is accessible
    if not check_elasticsearch_connection(host, port):
        return False
    
    base_url = f'http://{host}:{port}'
    index_url = f'{base_url}/{index_name}'
    
    # Updated settings for Elasticsearch 8.x
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": "30s",
            "max_result_window": 50000,  # Increase for large datasets
            "analysis": {
                "analyzer": {
                    "standard_analyzer": {
                        "type": "standard",
                        "stopwords": "_english_"
                    }
                }
            }
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
                    },
                    "analyzer": "standard_analyzer"
                },
                "region_txt": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    },
                    "analyzer": "standard_analyzer"
                },
                "provstate": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "city": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "attacktype1_txt": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    },
                    "analyzer": "standard_analyzer"
                },
                "targtype1_txt": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "gname": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "weaptype1_txt": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "nkill": {"type": "integer"},
                "nwound": {"type": "integer"},
                "casualties": {"type": "integer"},
                "timestamp": {
                    "type": "date",
                    "format": "yyyy-MM-dd||yyyy-MM-dd HH:mm:ss||epoch_millis"
                },
                "location": {"type": "geo_point"},
                "summary": {
                    "type": "text",
                    "analyzer": "standard_analyzer"
                },
                "success": {"type": "boolean"},
                "suicide": {"type": "boolean"},
                "extended": {"type": "boolean"}
            }
        }
    }
    
    try:
        # Check if index exists and delete if needed
        check_response = requests.head(index_url, timeout=10)
        if check_response.status_code == 200:
            requests.delete(index_url, timeout=10)
        
        # Create new index
        create_response = requests.put(
            index_url, 
            json=index_settings,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        if create_response.status_code == 200:
            print(f"Index '{index_name}' created successfully")
            return True
        else:
            print(f"Failed to create index: {create_response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error setting up index: {e}")
        return False

def verify_index_setup(host='localhost', port=9200, index_name='terrorism'):
    """Verify that the index was created correctly"""
    try:
        response = requests.get(f'http://{host}:{port}/{index_name}', timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error verifying index: {e}")
        return False

def main():
    """Main function to set up and verify Elasticsearch index"""
    HOST = 'localhost'
    PORT = 9200
    INDEX_NAME = 'terrorism'
    
    if setup_elasticsearch_index(HOST, PORT, INDEX_NAME):
        if verify_index_setup(HOST, PORT, INDEX_NAME):
            print("Setup completed successfully")
        else:
            print("Setup completed but verification failed")
    else:
        print("Setup failed")

if __name__ == "__main__":
    main()