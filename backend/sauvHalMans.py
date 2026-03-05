import requests
import json
import time

def download_hal_data(query='structName_t:"*le mans*"', filename="ressources/halLeMans.json"):
    base_url = "https://api.archives-ouvertes.fr/search/"
    rows_per_page = 1000  # Taille du paquet
    start = 0
    all_docs = []
    
    print(f"Début de la récupération dans : {filename}")

    while True:
        params = {
            "q": query,
            "fl": "structId_i,label_s,structAddress_s,structName_s,keyword_s,docType_s,producedDateY_i,producedDateM_i",
            "rows": rows_per_page,
            "start": start,
            "wt": "json"
        }

        try:
            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            docs = data.get("response", {}).get("docs", [])
            num_found = data.get("response", {}).get("numFound", 0)
            
            if not docs:
                break
            
            all_docs.extend(docs)
            print(f"Progression : {len(all_docs)} / {num_found}")

            # Arrêt si on a tout récupéré
            if len(all_docs) >= num_found:
                break
            
            # Mise à jour de l'index de départ pour la page suivante
            start += rows_per_page
            
            # Petite pause pour être poli avec le serveur
            time.sleep(0.1) 

        except Exception as e:
            print(f"Erreur lors de la requête : {e}")
            break

    # Sauvegarde finale
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_docs, f, ensure_ascii=False, indent=4)
    
    print(f"\nTerminé ! {len(all_docs)} projets sauvegardés dans '{filename}'.")

if __name__ == "__main__":
    download_hal_data()