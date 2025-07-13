
import requests

index_settings = {
  "mappings": {
    "properties": {
      "eventid": {"type": "keyword"},
      "iyear": {"type": "integer"},
      "country_txt": {"type": "text"},
      "region_txt": {"type": "text"},
      "attacktype1_txt": {"type": "text"},
      "casualties": {"type": "integer"}
    }
  }
}

res = requests.put('http://localhost:9200/terrorism', json=index_settings)
print(res.json())
