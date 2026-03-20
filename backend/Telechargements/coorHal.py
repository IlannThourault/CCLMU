import json
import re
import requests
from concurrent.futures import ThreadPoolExecutor

# Configuration
INPUT_FILE = "halLeMans.json"
OUTPUT_FILE = "CCLMU/public/coorHal.json"
MAX_WORKERS = 20 

geo_cache = {}
referentiel_noms = {} # Pour stabiliser les coordonnées d'un même nom

def get_coordinates(adresse):
    addr_clean = " ".join(re.sub(r'(?i)(cedex|BP|CS)\s*\d+', '', adresse).split())
    if addr_clean in geo_cache: return geo_cache[addr_clean]
    try:
        resp = requests.get("https://api-adresse.data.gouv.fr/search/", params={"q": addr_clean, "limit": 1}, timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            if data['features']:
                coords = data['features'][0]['geometry']['coordinates']
                res = [coords[1], coords[0]]
                geo_cache[addr_clean] = res
                return res
    except: pass
    geo_cache[addr_clean] = None
    return None

def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            docs = json.load(f)
    except FileNotFoundError:
        print(f"Erreur : {INPUT_FILE} introuvable.")
        return

    # 1. Géocodage
    all_addresses = set()
    for d in docs:
        for addr in d.get("structAddress_s", []):
            all_addresses.add(addr)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(get_coordinates, list(all_addresses))

    # 2. Fusion par clé (Nom, Latitude, Longitude)
    fusion_dict = {}

    for d in docs:
        nom_org = d.get("structName_s", "Inconnu")
        if isinstance(nom_org, list): nom_org = nom_org[0]
        
        for addr in d.get("structAddress_s", []):
            c = geo_cache.get(addr)
            if c:
                # Stabilisation des coordonnées par nom
                if nom_org not in referentiel_noms:
                    referentiel_noms[nom_org] = c
                
                lat, lon = referentiel_noms[nom_org]
                
                # CLÉ UNIQUE : Nom + GPS
                cle_unique = (nom_org, lat, lon)
                
                if cle_unique not in fusion_dict:
                    fusion_dict[cle_unique] = {
                        "gps": [[lat, lon]],
                        "n": nom_org,
                        "y": set(), # On utilise des sets pour collecter sans doublons
                        "m": set(),
                        "kw": set()
                    }
                
                # Accumulation des données
                fusion_dict[cle_unique]["y"].add(d.get("producedDateY_i", 0))
                fusion_dict[cle_unique]["m"].add(d.get("producedDateM_i", 0))
                
                kws = d.get("keyword_s", [])
                if isinstance(kws, str): kws = [kws]
                for k in kws:
                    fusion_dict[cle_unique]["kw"].add(k)

    # 3. Formatage final
    web_data = []
    for item in fusion_dict.values():
        # Conversion des sets en listes pour le JSON
        item["y"] = list(item["y"])
        item["m"] = list(item["m"])
        item["kw"] = list(item["kw"])
        web_data.append(item)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(web_data, f, indent=2, ensure_ascii=False)
    
    print(f"Fichier généré : {len(web_data)} entités géographiques uniques.")

if __name__ == "__main__":
    main()