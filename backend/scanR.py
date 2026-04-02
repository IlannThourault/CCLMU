import requests
import json
from dotenv import load_dotenv
import os

# Chargement de .private_env
if os.path.exists(".private_env"):
    load_dotenv(".private_env")
elif os.path.exists("../.private_env"):
    load_dotenv("../.private_env")
else:
    print("Error: .private_env file not found")
    exit()

# Chargement de l'username et du password
username = os.getenv("SCANR_USERNAME")
password = os.getenv("SCANR_PASSWORD")

if username is None:
  print("Error : Failed to fetch .private_env::SCANR_USERNAME")
  exit()
if password is None:
  print("Error : Failed to fetch .private_env::SCANR_PASSWORD")
  exit()

url = "https://cluster-production.elasticsearch.dataesr.ovh/scanr-organizations/_search"
headers = {
    "Content-Type": "application/json",
}


# Récupération du nombre de résultâts
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


size = response.json()["hits"]["total"]["value"]

# Requete avec la bonne taille
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
  })
)


def get_markers(marker): # temp
    return body[marker]