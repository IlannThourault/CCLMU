"""
Module de gestion des données ScanR (Système de Cartographie Nationale de la Recherche)
Fournit des fonctions pour accéder aux données d'organisations de recherche françaises
Via une requête API Elasticsearch au serveur ScanR en production

NOTE : Module actuellement non utilisé dans l'application
"""

import requests
import json
from dotenv import load_dotenv
import os

# ========== CHARGEMENT DE LA CONFIGURATION ==========

# Chargement du fichier .private_env contenant les identifiants d'authentification
# Le fichier peut être à la racine du projet backend ou au niveau parent
if os.path.exists(".private_env"):
    load_dotenv(".private_env")
elif os.path.exists("../.private_env"):
    load_dotenv("../.private_env")
else:
    print("Error: .private_env file not found")
    exit()

# ========== AUTHENTIFICATION ==========

# Récupération des identifiants depuis les variables d'environnement
username = os.getenv("SCANR_USERNAME")
password = os.getenv("SCANR_PASSWORD")

if username is None:
    print("Error : Failed to fetch .private_env::SCANR_USERNAME")
    exit()
if password is None:
    print("Error : Failed to fetch .private_env::SCANR_PASSWORD")
    exit()

# ========== CONFIGURATION API ==========

# URL de l'API Elasticsearch de ScanR en production
url = "https://cluster-production.elasticsearch.dataesr.ovh/scanr-organizations/_search"

# Headers HTTP pour les requêtes
headers = {
    "Content-Type": "application/json",
}

# ========== REQUETE 1 : RECUPERATION DU NOMBRE DE RESULTATS ==========

# Première requête : compte le nombre total d'organisations match "Le Mans"
# avec size=0 pour ne récupérer que le count sans les données
response = requests.post(
    url,
    auth=(username, password),  # Authentification basique HTTP
    headers=headers,
    data=json.dumps({
        "size": 0,  # Ne pas récupérer de résultats, juste le count
        "query": {
            "query_string": {
                "fields": ["address.city"],  # Recherche dans le champ city
                "query": "\"Le Mans\""  # Requête : ville exactement "Le Mans"
            }
        }
    })
)

# Extraction du nombre total de résultats
size = response.json()["hits"]["total"]["value"]

# ========== REQUETE 2 : RECUPERATION DE TOUS LES RESULTATS ==========

# Deuxième requête : récupère tous les résultats avec le count exact calculé précédemnent
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
        "from": 0,  # Index de départ
        "size": size  # Nombre de résultats à récupérer
    })
)

# ========== FONCTIONS PUBLIQUES ==========

def get_markers(marker):
    """
    Fonction temporaire pour extraire une clé spécifique des résultats
    
    Parameters:
        marker (str): La clé à extraire du corps de réponse
    
    Returns:
        Valeur associée à la clé marker
    
    NOTE : Function non complète, référence une variable 'body' non definie
    """
    # TODO: Correction nécessaire - la variable 'body' n'existe pas
    return body[marker]