import re
import json
from collections import Counter

# Chargement des données
# Assurez-vous que les chemins correspondent à votre structure de projet
with open("../public/coorHal.json", "r") as f:
    data = json.load(f)

with open("../../halLeMans.json", "r") as hal_file:
    dataHal = json.load(hal_file)

def getCoordinatesFromDates(anneeMin, anneeMax, moisMin, moisMax):
    """Renvoie la liste unique des points GPS pour une période donnée."""
    results = []
    for d in data:
        if anneeMin <= d.get('y', 0) <= anneeMax:
            if moisMin <= d.get('m', 0) <= moisMax:
                for coord in d.get('gps', []):
                    results.append(tuple(coord))
    return list(set(results))

def getAllKeyWords():
    """Génère le fichier de suggestions pour la barre de recherche."""
    tous_les_mots_trouves = []
    pattern = r'^[a-zA-Z0-9àâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ\s\-,.\'\(\)]+$'

    for d in dataHal:
        mots = d.get("keyword_s", [])
        if isinstance(mots, str):
            mots = [mots]
        
        if isinstance(mots, list):
            for m in mots:
                if re.match(pattern, m):
                    tous_les_mots_trouves.append(m.strip())

    compteur = Counter(tous_les_mots_trouves)
    mots_tries_par_frequence = [mot for mot, count in compteur.most_common()]

    chemin = "ressources/keywordsHal.ts"
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("export const HalKeywords: string[] = [\n")
        for kw in mots_tries_par_frequence:
            clean_kw = kw.replace("'", "\\'")
            f.write(f"  '{clean_kw}',\n")
        f.write("];\n")



# Dans hal.py, modifiez la fonction getDataFromFilters
def getDataFromFilters(anneeMin, anneeMax, moisMin, moisMax, selectedKeywords=None):
    results = []
    vus = set()
    search_terms = [s.strip().lower() for s in selectedKeywords] if selectedKeywords else []

    for d in data:
        # Récupération de l'année (qui est maintenant une liste grâce à coorHal.py)
        annees_projet = d.get('y', [])
        if isinstance(annees_projet, int): annees_projet = [annees_projet]
        
        # 1. Filtre sur les dates : on vérifie si une des années est dans la plage
        date_match = any(anneeMin <= a <= anneeMax for a in annees_projet)
        
        if date_match:
            # 2. Logique de filtrage par mots-clés
            match = True
            if search_terms:
                entree_kws = d.get('kw', [])
                if entree_kws is None: entree_kws = []
                entree_kws_lower = [str(k).lower() for k in entree_kws]
                
                match = any(
                    any(term in project_kw for project_kw in entree_kws_lower)
                    for term in search_terms
                )
            
            # 3. Construction du format de sortie
            if match:
                nom_org = d.get('n', "Inconnu")
                coords = d.get('gps', [])
                
                # 'gps' est une liste de listes [[lat, lon]]
                for c in coords:
                    nom_lat_long_str = f"{nom_org},{c[0]},{c[1]}"
                    if nom_lat_long_str not in vus:
                        results.append([nom_lat_long_str])
                        vus.add(nom_lat_long_str)
    
    return results