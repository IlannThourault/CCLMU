import requests
import json
from dotenv import load_dotenv
import os

# Charger le .env
if os.path.exists(".private_env"):
    load_dotenv(".private_env")
elif os.path.exists("../.private_env"):
    load_dotenv("../.private_env")
else:
    print("Error: .private_env file not found")
    exit()

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

print("Envoie")

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


print("Status code:", response.status_code)
print("Response body:", response.json()["hits"]["hits"][0])


"""
load_dotenv("../.private_env")

username = os.getenv("SCANR_USERNAME")
password = os.getenv("SCANR_PASSWORD")

URL = "https://cluster-production.elasticsearch.dataesr.ovh/scanr-publications/_search"

headers = {
    "Content-Type": "application/json"
}

query_base = {
    "size": 1000,
    "sort": [
        {"publicationDate": "asc"}
    ],
    "query": {
        "match": {
            "affiliations.mainAddress.city": "Le Mans"
        }
    }
}

all_results = []
search_after = None

while True:

    query = query_base.copy()

    if search_after:
        query["search_after"] = search_after

    r = requests.post(
        URL,
        auth=(username, password),
        headers=headers,
        json=query
    )

    if r.status_code != 200:
        print("Erreur HTTP:", r.status_code)
        print(r.text)
        break

    data = r.json()

    hits = data.get("hits", {}).get("hits", [])

    if not hits:
        break

    all_results.extend(hits)

    search_after = hits[-1]["sort"]

    print("Total récupéré :", len(all_results))

print("Terminé :", len(all_results))

with open("scanr_publications_le_mans.json", "w") as f:
    json.dump(all_results, f)
"""
"""
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv("../.private_env")

username = os.getenv("SCANR_USERNAME")
password = os.getenv("SCANR_PASSWORD")

URL = "https://cluster-production.elasticsearch.dataesr.ovh/scanr-publications/_search"

headers = {
    "Content-Type": "application/json"
}

query_base = {
    "size": 1000,
    "sort": [
        {"publicationDate": "asc"}
    ],
    "_source": [
        "title",
        "affiliations.address",
        "affiliations.mainAddress",
        "affiliations.coordinates",
        "affiliations.kind",
        "affiliations.id",
        "affiliations.acronym.default",
        "landingPage",
        "keywords",
        "domains",
        "summary.default",
        "projects.id"
    ],
    "query": {
        "match": {
            "affiliations.mainAddress.city": "Le Mans"
        }
    }
}

all_results = []
search_after = None

while True:

    query = dict(query_base)

    if search_after:
        query["search_after"] = search_after

    r = requests.post(
        URL,
        auth=(username, password),
        headers=headers,
        json=query
    )

    data = r.json()
    hits = data.get("hits", {}).get("hits", [])

    if not hits:
        break

    for h in hits:
        src = h["_source"]

        publication = {
            "title": src.get("title"),
            "landing_page": src.get("landingPage"),
            "summary": src.get("summary", {}).get("default"),
            "keywords": [k.get("label") for k in src.get("keywords", []) if "label" in k],
            "domains": [d.get("label") for d in src.get("domains", []) if "label" in d],
            "projects": [p.get("id") for p in src.get("projects", []) if "id" in p],
            "affiliations": []
        }

        for aff in filter(None, src.get("affiliations", [])):
          main_address = aff.get("mainAddress") or {}
          publication["affiliations"].append({
              "id": aff.get("id"),
              "kind": aff.get("kind"),
              "acronym": aff.get("acronym", {}).get("default"),
              "address": aff.get("address"),
              "city": main_address.get("city"),
              "coordinates": aff.get("coordinates")
          })

        all_results.append(publication)

    search_after = hits[-1]["sort"]

    print("Total récupéré :", len(all_results))

print("Terminé :", len(all_results))

with open("publications_le_mans_light.json", "w") as f:
    json.dump(all_results, f, indent=2)

"""


def get_markers():
    return [
        {"lat": 48.0061, "lng": 0.1996, "title": "Le Mans"},
        {"lat": 48.008, "lng": 0.202, "title": "Point B"},
    ]