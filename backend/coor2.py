import json
import re
import requests

# --- GARDER VOS FONCTIONS DE NETTOYAGE ET GÉOCODAGE ---
def clean_address(adresse):
    if not adresse: return ""
    adresse = re.sub(r'(?i)cedex.*', '', adresse)
    adresse = re.sub(r'(?i)(BP|CS)\s*\d+', '', adresse)
    return " ".join(adresse.split())

def get_coordinates(adresse):
    # (Gardez votre fonction get_coordinates identique ici)
    # ...
    return None, None # (Simplifié pour l'exemple)

# --- NOUVELLE LOGIQUE DE CHARGEMENT ---

def load_data_from_json(filename="projets_hal_lemans.json"):
    """Charge les données sauvegardées localement"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {filename} est introuvable.")
        return []

def display_structures(documents, anneeMin, anneeMax, moisMin, moisMax):
    processed_partners = set()

    for doc in documents:
        annee = doc.get("producedDateY_i", 0)
        mois = doc.get("producedDateM_i", 0)
        names = doc.get("structName_s", [])
        addresses = doc.get("structAddress_s", [])
        keywords = doc.get("keyword_s", [])

        # On vérifie si ce document appartient bien à une structure du Mans
        has_mans = any("mans" in str(addr).lower() for addr in addresses)

        if has_mans:
            # On affiche les mots-clés du projet
            if keywords:
                print(f"\n Mots-clés : {', '.join(keywords)}")
                print(f" Année : {annee} / Mois : {mois}")
            else:
                print("pas de keyword")
            for i in range(len(names)):
                name_partenaire = names[i]
                addr_partenaire = addresses[i] if i < len(addresses) else ""

            # Filtrer pour ne garder que les partenaires HORS Le Mans
                p_key = f"{name_partenaire}-{addr_partenaire}"
                
                if p_key not in processed_partners:
                    print(f"   -> Partenaire : {name_partenaire}")
                    print(f"      Lieu : {addr_partenaire}")
                    
                    # Attention : Avec 48k projets, le géocodage peut être long.
                    # Vous devriez peut-être limiter le nombre de traitements.
                    lat, lon = get_coordinates(addr_partenaire)
                    if lat:
                        print(f"      GPS : {lat}, {lon}")
                    
                    processed_partners.add(p_key)
                    print("-" * 20)

def main():
    # 1. Charger les 48 000 résultats depuis le disque
    print("Chargement des données locales...")
    publications = load_data_from_json("ressources/halLeMans.json")
    print(f"{len(publications)} projets chargés.")

    # 2. Analyser les données (ex: sur les 500 premiers pour tester)
    # On utilise le 'slicing' [0:500] pour ne pas lancer 40 000 géocodages d'un coup
    display_structures(publications[0:500],0,0,0,0)

if __name__ == "__main__":
    main()