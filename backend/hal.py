"""
Module de gestion des données HAL (Hyper Articles en Ligne)
Fournit des fonctions pour accéder et filtrer les données de publications scientifiques
Les données sont stockées dans un fichier JSON '../public/coorHal.json'
HAL est l'archive ouverte multidisciplinaire française pour les publications scientifiques
"""

import re
import json
from collections import Counter
import requests

# ========== INITIALISATION DES DONNEES ==========
# Chargement du fichier JSON contenant les publications HAL et leurs géolocalisations
with open("../public/coorHal.json", "r") as f:
    data = json.load(f)

# ========== RECHERCHE DE COORDONNEES GEOGRAPHIQUES ==========

def getCoordinatesFromDates(anneeMin, anneeMax, moisMin, moisMax):
    """
    Récupère tous les points GPS des publications HAL réalisées dans une plage de dates
    
    Parameters:
        anneeMin (int): Année minimale
        anneeMax (int): Année maximale
        moisMin (int): Mois minimum (1-12)
        moisMax (int): Mois maximum (1-12)
    
    Returns:
        list: Liste de tuples uniques (latitude, longitude) de coordonnées GPS
    """
    results = []
    for d in data:
        if anneeMin <= d.get('y', 0) <= anneeMax:
            if moisMin <= d.get('m', 0) <= moisMax:
                for coord in d.get('gps', []):
                    results.append(tuple(coord))
    return list(set(results))


# ========== GESTION DES MOTS-CLES ==========

def getAllKeyWords():
    """
    Extrait tous les mots-clés unique de HAL, les filtre par pattern regex valide,
    les compte, les trie par fréquence, et exporte le résultat dans un fichier TypeScript
    
    Validation : Seules les lettres, chiffres, accents français et caractères spéciaux 
    (tiret, point, virgule, apostrophe, parenthèses) sont acceptés
    
    Returns:
        None
    
    Side effects:
        Crée/écrase le fichier 'ressources/keywordsHal.ts' avec l'export TypeScript
    """
    tous_les_mots_trouves = []
    # Pattern regex pour accepter seulement les caractères valides
    pattern = r'^[a-zA-Z0-9àâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ\s\-,.\'\(\)]+$'

    for d in dataHal:
        mots = d.get("keyword_s", [])
        if isinstance(mots, str):
            mots = [mots]
        
        if isinstance(mots, list):
            for m in mots:
                if re.match(pattern, m):
                    tous_les_mots_trouves.append(m.strip())

    # Comptage des fréquences et tri décroissant
    compteur = Counter(tous_les_mots_trouves)
    mots_tries_par_frequence = [mot for mot, count in compteur.most_common()]

    # Export en fichier TypeScript
    chemin = "ressources/keywordsHal.ts"
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("export const HalKeywords: string[] = [\n")
        for kw in mots_tries_par_frequence:
            clean_kw = kw.replace("'", "\\'")  # Échappe les apostrophes pour TypeScript
            f.write(f"  '{clean_kw}',\n")
        f.write("];\n")


# ========== ACCESSEURS DE DATES EXTREMES ==========

def getFirstMonth():
    """
    Récupère le mois de la première (plus ancienne) publication HAL
    
    Returns:
        int: Le mois (1-12) ou None si aucune donnée disponible
    """
    all_dates = []
    
    for project in data:
        years = project.get("y", [])
        months = project.get("m", [])
        
        if isinstance(years, list) and isinstance(months, list) and years:
            project_min_date = min(zip(years, months))
            all_dates.append(project_min_date)

    if not all_dates:
        return None

    return min(all_dates)[1]


def getFirstYear():
    """
    Récupère l'année de la première (plus ancienne) publication HAL
    
    Returns:
        int: L'année ou None si aucune donnée disponible
    """
    all_dates = []
    
    for project in data:
        years = project.get("y", [])
        months = project.get("m", [])
        
        if isinstance(years, list) and isinstance(months, list) and years:
            project_min_date = min(zip(years, months))
            all_dates.append(project_min_date)

    if not all_dates:
        return None

    return min(all_dates)[0]


# ========== FILTRAGE AVANCE DE DONNEES ==========

def getDataFromFilters(anneeMin, anneeMax, moisMin, moisMax, keyword1=None, keyword2=None):
    """
    Récupère les données de publications filtées par date ET optionnellement par mots-clés
    Les résultats sont retournés avec les coordonnées GPS asociées
    
    Parameters:
        anneeMin (int): Année minimale
        anneeMax (int): Année maximale
        moisMin (int): Mois minimum (0-12 où 0 = début d'année)
        moisMax (int): Mois maximum (1-12)
        keyword1 (str, optional): Premier mot-clé à rechercher (case-insensitive)
        keyword2 (str, optional): Second mot-clé à rechercher (case-insensitive)
    
    Returns:
        list: Liste de chaînes au format 'nom_organisation,latitude,longitude'
              Les doublons sont éliminés automatiquement
    """
    results = []
    vus = set()  # Ensembles de tuples déjà trouvées pour éviter les doublons
    
    # Filtration des mots-clés vides
    search_terms = [str(k).strip().lower() for k in [keyword1, keyword2] if k and str(k).strip()]

    for d in data:
        # ===== FILTRAGE PAR DATE =====
        annees_projet = d.get('y', [])
        if isinstance(annees_projet, (int, float)): 
            annees_projet = [annees_projet]
        
        date_match = any(anneeMin <= int(a) <= anneeMax for a in annees_projet if str(a).isdigit())
        
        if date_match:
            match = True
            
            # ===== FILTRAGE PAR MOTS-CLES =====
            if search_terms:
                entree_kws = d.get('kw') or []
                entree_kws_lower = [str(k).lower() for k in entree_kws]
                
                # Vérifie que TOUS les mots-clés sont presentes au moins une fois
                match = all(
                    any(term in project_kw for project_kw in entree_kws_lower)
                    for term in search_terms
                )
            
            # ===== AJOUT AUX RESULTATS =====
            if match:
                nom_org = str(d.get('n', "Inconnu")).replace(",", " ")  # Échappe les virgules
                coords = d.get('gps', [])
                
                for c in coords:
                    if len(c) >= 2:
                        nom_lat_long_str = f"{nom_org},{c[0]},{c[1]}"
                        if nom_lat_long_str not in vus:
                            results.append(nom_lat_long_str) 
                            vus.add(nom_lat_long_str)
    
    return results


# ========== REQUETES API HAL EXTERNE ==========

def getProjectsFromCollab(nomOrga, limite=5):
    #retourne les porjets en collaboration d'une organisation avec le mans (même format que cordis)
    query = f'structName_t:"{nomOrga}" AND structName_t:"Mans"'

    # Champs à récupérer
    fields = "title_s,abstract_s,producedDate_s,authFullName_s,label_s,authStructName_s,structName_s"
    url = f"https://api.archives-ouvertes.fr/search/?q={query}&fl={fields}&rows={limite}&wt=json"

    listeProjects = []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            docs = response.json().get('response', {}).get('docs', [])
            for d in docs:
                # Extraction des champs
                title = d.get('title_s', ["Sans titre"])[0]
                abstract = d.get('abstract_s', ["Pas de résumé disponible"])[0]
                date_prod = d.get('producedDate_s', "2000-01-01")
                
                # Formatage de la date si seulement l'année est fournie
                if len(date_prod) == 4: 
                    date_prod += "-01-01"
                
                # Contributors peuvent être au champ authStructName_s ou structName_s
                contributors = d.get("authStructName_s") or d.get("structName_s") or []

                unique_contributors = sorted(list(set(contributors)))
                listeProjects.append({
                    "title": title,
                    "teaser": d.get('label_s', "")[:200] + "...",  # Citation limitée à 200 chars
                    "description": abstract,
                    "date": date_prod,
                    "cout" : "pas d'informations (hal)",
                    "allContributors": unique_contributors
                })
    except Exception as e:
        print(f"Erreur lors de la requête HAL : {e}")

    return listeProjects

