import requests
import json
from dotenv import load_dotenv
import os

# Charger le .env (depuis la racine)
load_dotenv("../.private_env")

username = os.getenv("SCANR_USERNAME")
password = os.getenv("SCANR_PASSWORD")

url = "https://cluster-production.elasticsearch.dataesr.ovh/scanr-organizations/_search"

headers = {
    "Content-Type": "application/json",
}  

# Get the size of the data set
response = requests.post(
  url,
  auth=(username, password),
  headers=headers,
  data=json.dumps({
  "size": 0,
    "query": {
      "query_string": {
        "fields": ["address.city"],
        "query": "\"Le Mans\""
      }
    }
  })
)

print("Status code:", response.status_code)
print(response.json().keys())
size = response.json()["hits"]["total"]["value"]
print("Response body:", size)#response.text)

# Faire la requête POST
response = requests.post(
    url,
    auth=(username, password),  # Basic Auth
    headers=headers,
    data=json.dumps({
    "query": {
      "query_string": {
        "fields": ["address.city"],
        "query": "\"Le Mans\""
      }
    },
    "from": 0,
    "size": size
  })    # raw body JSON
)

# Vérifier la réponse
print("Status code:", response.status_code)
print("Response body:", response) #response.text)

def get_markers():
    return [
        {"lat": 48.0061, "lng": 0.1996, "title": "Le Mans"},
        {"lat": 48.008, "lng": 0.202, "title": "Point B"},
    ]