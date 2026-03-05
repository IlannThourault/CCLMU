import requests
import re
import time

# URLs
search_api = "https://api.archives-ouvertes.fr/search/"

def clean_address(adresse):
    if not adresse: return ""
    adresse = re.sub(r'(?i)cedex.*', '', adresse)
    adresse = re.sub(r'(?i)(BP|CS)\s*\d+', '', adresse)
    return " ".join(adresse.split())

def get_coordinates(adresse):
    if not adresse or adresse == "Adresse inconnue": return None, None
    adresse_propre = clean_address(adresse)
    
    # API France
    url_fr = "https://api-adresse.data.gouv.fr/search/"
    try:
        resp = requests.get(url_fr, params={"q": adresse_propre, "limit": 1}, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data['features']:
                coords = data['features'][0]['geometry']['coordinates']
                return coords[1], coords[0]
    except: pass

    # Nominatim
    url_global = "https://nominatim.openstreetmap.org/search"
    headers = {'User-Agent': 'MonProjetRecherche-LeMans'}
    try:
        resp = requests.get(url_global, params={"q": adresse_propre, "format": "json", "limit": 1}, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except: pass
    return None, None

def get_structures(query="le mans", rows=50):
    # AJOUT de keyword_s dans le champ fl
    params = {
        "q": query, 
        "fl": "structId_i,label_s,structAddress_s,structName_s,keyword_s,title_s", 
        "rows": rows, 
        "wt": "json"
    }
    response = requests.get(search_api, params=params)
    return response.json().get("response", {}).get("docs", [])

def display_structures(documents):
    mots_cles = set()
    processed_partners = set()

    for doc in documents:
        names = doc.get("structName_s", [])
        addresses = doc.get("structAddress_s", [])
        # Récupération des mots-clés du projet (liste)
        keywords = doc.get("keyword_s", [])
        title = doc.get("title_s", ["Sans titre"])[0]

        has_mans = any("mans" in str(addr).lower() for addr in addresses)

        if has_mans:
            for i in range(len(names)):
                name_partenaire = names[i]
                addr_partenaire = addresses[i] if i < len(addresses) else ""

                if "mans" not in str(addr_partenaire).lower() and addr_partenaire:
                    p_key = f"{name_partenaire}-{addr_partenaire}"
                    
                    if p_key not in processed_partners:
                        """print(f" Partenaire trouvé : {name_partenaire}")
                        print(f"   Lieu : {addr_partenaire}")
                        print(f"   Projet : {title}")
                        """
                        # Affichage propre des mots-clés
                        if keywords:
                            #print(f"    Mots-clés : {', '.join(keywords)}")
                            mots_cles.update(keywords)
                        #else:
                            #print(f"    Mots-clés : Aucun trouvé")
                        
                        lat, lon = get_coordinates(addr_partenaire)
                        """if lat:
                            print(f"    GPS : {lat}, {lon}")
                        else:
                            print(f"    GPS : Non trouvé")
                        """
                        processed_partners.add(p_key)
                        #print("-" * 30)
                    
    print("\nMots-clés trouvés :")
    for m in mots_cles:
        print(m)

def main():
    publications = get_structures(rows=100)
    display_structures(publications)

if __name__ == "__main__":
    main()