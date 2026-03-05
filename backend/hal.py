
import json



"""
import re
import requests
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
FILE_PATH = "ressources/halLeMans.json"
MAX_WORKERS = 10  # Nombre de requêtes simultanées (ne pas trop monter pour ne pas être banni)

# Cache global pour éviter de chercher deux fois la même adresse
geo_cache = {}

def clean_address(adresse):
    if not adresse: return ""
    adresse = re.sub(r'(?i)cedex.*', '', adresse)
    adresse = re.sub(r'(?i)(BP|CS)\s*\d+', '', adresse)
    return " ".join(adresse.split())

def get_coordinates(adresse):
    #Fonction de géocodage unitaire avec cache intégré
    if not adresse or adresse == "Adresse inconnue": return None
    
    adresse_propre = clean_address(adresse)
    if adresse_propre in geo_cache:
        return geo_cache[adresse_propre]

    url_fr = "https://api-adresse.data.gouv.fr/search/"
    try:
        resp = requests.get(url_fr, params={"q": adresse_propre, "limit": 1}, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if data['features']:
                coords = data['features'][0]['geometry']['coordinates']
                res = (coords[1], coords[0])
                geo_cache[adresse_propre] = res
                return res
    except: pass
    
    geo_cache[adresse_propre] = None
    return None

def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur chargement : {e}")
        return []

def process_doc(doc, anneeMin, anneeMax, moisMin, moisMax):
    #Filtre un document et extrait les adresses à géocoder
    annee = doc.get("producedDateY_i", 0)
    mois = doc.get("producedDateM_i", 0)

    # Filtre temporel
    if not (anneeMin <= annee <= anneeMax): return []
    if annee == anneeMin and moisMin > 0 and mois < moisMin: return []
    if annee == anneeMax and moisMax > 0 and mois > moisMax: return []

    addresses = doc.get("structAddress_s", [])
    names = doc.get("structName_s", [])
    
    # On vérifie si le projet est lié au Mans
    if any("mans" in str(addr).lower() for addr in addresses):
        # On retourne la liste des adresses des partenaires hors Le Mans
        return [addr for addr in addresses if "mans" not in str(addr).lower()]
    return []

"""

with open("ressources/coorHal.json", "r") as f:
        data = json.load(f)

def getCoordinatesFromDates(anneeMin, anneeMax, moisMin, moisMax):
    
    
    results = []
    for d in data:
        if anneeMin <= d['y'] <= anneeMax:
            if moisMin <= d['m'] <= moisMax:
                for coord in d['gps']:
                    results.append(tuple(coord))
    
    return list(set(results))