import re
import json
from collections import Counter
import requests

# Chargement des données
with open("../public/coorHal.json", "r") as f:
    data = json.load(f)


def getCoordinatesFromDates(anneeMin, anneeMax, moisMin, moisMax):
    results = []
    for d in data:
        if anneeMin <= d.get('y', 0) <= anneeMax:
            if moisMin <= d.get('m', 0) <= moisMax:
                for coord in d.get('gps', []):
                    results.append(tuple(coord))
    return list(set(results))

def getAllKeyWords():
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




def getFirstMonth():
    all_dates = []
    
    for project in data:
        years = project.get("y", [])
        months = project.get("m", [])
        
        if isinstance(years, list) and isinstance(months, list) and years:
            project_min_date = min(zip(years, months))
            all_dates.append(project_min_date)

    if not all_dates:
        return None, None

    return min(all_dates)[1]

def getFirstYear():
    all_dates = []
    
    for project in data:
        years = project.get("y", [])
        months = project.get("m", [])
        
        if isinstance(years, list) and isinstance(months, list) and years:
            project_min_date = min(zip(years, months))
            all_dates.append(project_min_date)

    if not all_dates:
        return None, None

    return min(all_dates)[0]

# Dans hal.py, modifiez la fonction getDataFromFilters
def getDataFromFilters(anneeMin, anneeMax, moisMin, moisMax, keyword1=None, keyword2=None):
    results = []
    vus = set()
    
    # On récupère uniquement les mots-clés non vides
    search_terms = [str(k).strip().lower() for k in [keyword1, keyword2] if k and str(k).strip()]

    for d in data:
        # filtrage des dates
        annees_projet = d.get('y', [])
        if isinstance(annees_projet, (int, float)): 
            annees_projet = [annees_projet]
        
        date_match = any(anneeMin <= int(a) <= anneeMax for a in annees_projet if str(a).isdigit())
        
        if date_match:
            match = True
            if search_terms:
                entree_kws = d.get('kw') or []
                entree_kws_lower = [str(k).lower() for k in entree_kws]
                
                #filtrage des mots clés
                match = all(
                    any(term in project_kw for project_kw in entree_kws_lower)
                    for term in search_terms
                )
            
            #ajout à la liste de retour
            if match:
                nom_org = str(d.get('n', "Inconnu")).replace(",", " ")
                coords = d.get('gps', [])
                
                for c in coords:
                    if len(c) >= 2:
                        nom_lat_long_str = f"{nom_org},{c[0]},{c[1]}"
                        if nom_lat_long_str not in vus:
                            results.append(nom_lat_long_str) 
                            vus.add(nom_lat_long_str)
    
    return results


#de base à 5 pour limiter le temps de réponse de l'api
def getProjectsFromCollab(nomOrga, limite=5):
    #retourne les porjets en collaboration d'une organisation avec le mans (même format que cordis)
    query = f'structName_s:"{nomOrga}"'

    fields = "title_s,abstract_s,producedDate_s,authFullName_s,label_s,authStructName_s,structName_s"
    url = f"https://api.archives-ouvertes.fr/search/?q={query}&fl={fields}&rows={limite}&wt=json"

    listeProjects = []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            docs = response.json().get('response', {}).get('docs', [])
            
            for d in docs:
                title = d.get('title_s', ["Sans titre"])[0]
                abstract = d.get('abstract_s', ["Pas de résumé disponible"])[0]
                date_prod = d.get('producedDate_s', "2000-01-01")
                #formatage de la date
                if len(date_prod) == 4: date_prod += "-01-01"
                
                contributors = d.get("authStructName_s") or d.get("structName_s") or []


                listeProjects.append({
                    "title": title,
                    "teaser": d.get('label_s', "")[:200] + "...", # Un extrait de la citation
                    "description": abstract,
                    "date": date_prod,
                    "allContributors": contributors
                })
    except Exception as e:
        print(f"Erreur lors de la requête HAL : {e}")

    return listeProjects


###Tests

#print(getDataFromFilters(1900, 2030, 0, 12, "le mans"))

org = "Dpt Néphrologie Dialyse Transplantation [CHU Angers]"


#print(getProjectsFromCollab(org, 10))