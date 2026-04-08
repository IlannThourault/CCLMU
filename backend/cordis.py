"""
Module de gestion des données CORDIS (Community Research and Development Information Service)
Fournit des fonctions pour accéder et filtrer les données de projets de recherche européens.
Les données sont stockées dans un fichier JSON 'ressources/publications.json'
"""

import json
import datetime
from collections import Counter
import pprint

# ========== INITIALISATION DES DONNEES ==========
# Chargement du fichier JSON contenant tous les projets CORDIS en mémoire
# Ce fichier est chargé une seule fois au démarrage du module pour optimiser les performances
with open("ressources/publications.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ========== FONCTIONS DE RECHERCHE BASIQUE ==========

def getProjectFromId(id: int):
    """
    Récupère un projet spécifique par son identifiant numérique
    
    Parameters:
        id (int): L'identifiant unique du projet CORDIS
    
    Returns:
        dict: Le dictionnaire du projet ou None si l'ID n'existe pas
    """
    id_str = str(id)
    return data.get(id_str)


def getAllLeMansOrganizations():
    """
    Récupère la liste de toutes les organisations ayant leur adresse au Mans
    qui ont participé à des projets CORDIS
    
    Returns:
        list: Liste unique des noms des organisations localisées au Mans
    """
    names = []

    for p in data.values():
        for orga in p["project"]["relations"]["associations"]["organization"]:
            if isinstance(orga, dict):  # on vérifie que c'est bien un dictionnaire
                if orga.get("address").get("city") == "Le Mans":
                    names.append(orga["legalName"])
    
    unique_names = list(set(names))
    return unique_names


def getAllLocalizations():
    """
    Récupère la liste de toutes les coordonnées géographiques (latitude, longitude)
    de toutes les organisations impliquées dans les projets CORDIS
    
    Returns:
        list: Liste unique de coordonnées géographiques
    """
    loc = []

    for p in data.values():
        for orga in p["project"]["relations"]["associations"]["organization"]:
            if isinstance(orga, dict):
                geo = orga.get("address").get("geolocation")
                if geo:
                    loc.append(geo)
    
    unique_loc = list(set(loc))
    return unique_loc


def getAllLocalizationsFrom1Project(project):
    """
    Extrait toutes les localisations (nom + coordonnées) des organisations d'un projet unique
    
    Parameters:
        project (dict): Le dictionnaire du projet CORDIS
    
    Returns:
        list: Liste unique de tuples (nom_organisation, coordonnées_GPS)
    """
    loc = []

    for orga in project["project"]["relations"]["associations"]["organization"]:
        if isinstance(orga, dict):
            geo = orga.get("address").get("geolocation")
            name = orga.get("legalName")
            if geo and name:
                loc.append((name, geo))
    
    unique_loc = list(set(loc))
    return unique_loc


def getAllOrganizationsFrom1Project(project):
    """
    Extrait la liste des noms de toutes les organisations participant à un projet
    
    Parameters:
        project (dict): Le dictionnaire du projet CORDIS
    
    Returns:
        list: Liste unique de noms d'organisations
    """
    names = []

    for orga in project["project"]["relations"]["associations"]["organization"]:
        if isinstance(orga, dict):
            name = orga.get("legalName")
            if name:
                names.append(name)
    
    unique_names = list(set(names))
    return unique_names


# ========== FONCTIONS UTILITAIRES DE DATES ==========

def createDateFromStr(dateStr):
    """
    Convertit une chaîne de caractères de date au format ISO (YYYY-MM-DD) 
    en objet datetime.date
    
    Parameters:
        dateStr (str): Date au format 'YYYY-MM-DD' (ex: '2020-03-15')
    
    Returns:
        datetime.date: L'objet date correspondant
    """
    year = int(dateStr[0:4]) 
    month = int(dateStr[5:7])
    day = int(dateStr[8:10])
    return datetime.date(year, month, day)


# ========== FILTRAGE PAR DATES ==========

def getAllLocalizationsFromDates(dateDebStr, dateFinStr, keywords):
    """
    Retourne les localisations de toutes les organisations ayant participé à des projets
    dont la date de réalisation se situe entre deux dates données, optionnellement filtrés par mots-clés
    
    Parameters:
        dateDebStr (str): Date de début au format 'YYYY-MM-DD'
        dateFinStr (str): Date de fin au format 'YYYY-MM-DD'
        keywords (str): Mots-clés séparés par des virgules pour filtrer (vide = sans filtre)
    
    Returns:
        list: Liste de chaînes au format 'nom_organisation,latitude,longitude'
    """
    loc = []

    dateDeb = createDateFromStr(dateDebStr)
    dateFin = createDateFromStr(dateFinStr)
    
    if keywords != "":          
        keywords = keywords.split(",")
        keyword1 = keywords[0].lower()
        keyword2 = keywords[-1].lower()

    for p in data.values():

        project = p["project"]

        dateDebTemp = createDateFromStr(project["startDate"])
        dateFinTemp = createDateFromStr(project["endDate"])

        if (dateDebTemp > dateDeb and dateDebTemp < dateFin) or \
           (dateFinTemp > dateDeb and dateFinTemp < dateFin):   

            listeKeywords = project.get("keywords", "").lower().split(",")

            # Suppression des espaces au début et à la fin
            listeKeywordsClear = [word.strip() for word in listeKeywords if word.strip()]
            if keywords == "":
                loc.extend(getAllLocalizationsFrom1Project(p))
            else:
                if keyword1 in listeKeywordsClear and keyword2 in listeKeywordsClear:
                    loc.extend(getAllLocalizationsFrom1Project(p))
    
    ens = list(set(loc))
    res = []

    for elem in ens:
        res.append(elem[0].replace(",", " ") + "," + elem[1])

    return res


# ========== FONCTIONS DE COLLABORATIONS ==========

# Fonction privée interne - Extraire les collaborateurs d'un seul projet
def getListContributors1Project(projet, nomOrga: str):
    """
    Extrait la liste des organisations qui collaborent avec une organisation donnée dans un projet
    (toutes les organisations SAUF celle passée en paramètre)
    
    Parameters:
        projet (dict): Le dictionnaire du projet
        nomOrga (str): Le nom de l'organisation principale (à exclure)
    
    Returns:
        list: Liste des noms des organisations collaboratrices
    """
    listContributors = []

    for orga in projet["project"]["relations"]["associations"]["organization"]:
        if isinstance(orga, dict):
            if orga.get("legalName") != nomOrga:
                listContributors.append(orga.get("legalName"))

    return listContributors


def getListContributors(nomOrga: str):
    """
    Récupère la liste complète de toutes les organisations qui collaborent avec une organisation donnée
    dans tous les projets CORDIS
    
    Parameters:
        nomOrga (str): Nom légal de l'organisation recherchée
    
    Returns:
        list: Liste unique de noms d'organisations collaboratrices
    """
    listContributors = []

    for p in data.values():
        for orga in p["project"]["relations"]["associations"]["organization"]:
            if isinstance(orga, dict):
                if orga.get("legalName") == nomOrga:
                    listContributors.extend(getListContributors1Project(p, nomOrga))

    
    unique_listContributors = list(set(listContributors))
    return unique_listContributors


def getLocFromName(nomOrga: str):
    """
    Récupère les coordonnées géographiques d'une organisation à partir de son nom
    
    Parameters:
        nomOrga (str): Nom légal de l'organisation
    
    Returns:
        str or tuple: Les coordonnées GPS (latitude, longitude) ou message d'erreur
    """
    for p in data.values():
        for orga in p["project"]["relations"]["associations"]["organization"]:
            if isinstance(orga, dict):
                if orga.get("legalName") == nomOrga:
                    return orga.get("address").get("geolocation")

    return "ERROR : Le nomOrga n'existe pas"


# ========== ORGANISATIONS MANOVA DU MANS ==========
# Organisations connues du Mans ayant participé à des projets CORDIS :
# - METACOUSTIC
# - Centre Hospitalier Le Mans
# - SILENTSYS
# - ACO AUTOMOBILE CLUB DE L'OUEST
# - GUATECS
# - COMMUNAUTE URBAINE DE LE MANS METROPOLE
# - UNIVERSITE DU MANS


# ========== ACCESSEURS DE DATES EXTREMES ==========

def getFirtDate():
    """
    Retourne la date de début la plus ancienne parmi tous les projets CORDIS
    
    Returns:
        datetime.date: La date minimale de démarrage de projet
    """
    firstDate = datetime.date(9999, 12, 31)

    for p in data.values():
        date_str = p["project"]["startDate"]

        year = int(date_str[0:4])
        month = int(date_str[5:7])
        day = int(date_str[8:10])

        dateTemp = datetime.date(year, month, day)

        if dateTemp < firstDate:
            firstDate = dateTemp
    
    return firstDate

def getFirstDateYear():
    """Retourne l'année de la date de début la plus ancienne"""
    return getFirtDate().year

def getFirstDateMonth():
    """Retourne le mois de la date de début la plus ancienne"""
    return getFirtDate().month

def getFirstDateDay():
    """Retourne le jour de la date de début la plus ancienne"""
    return getFirtDate().day


def getLastDate():
    """
    Retourne la date de fin la plus récente parmi tous les projets CORDIS
    
    Returns:
        datetime.date: La date maximale de fin de projet
    """
    lastDate = datetime.date(1, 1, 1)

    for p in data.values():
        date_str = p["project"]["endDate"]

        year = int(date_str[0:4])
        month = int(date_str[5:7])
        day = int(date_str[8:10])

        dateTemp = datetime.date(year, month, day)

        if dateTemp > lastDate:
            lastDate = dateTemp
    
    return lastDate

def getLastDateYear():
    """Retourne l'année de la date de fin la plus récente"""
    return getLastDate().year

def getLastDateMonth():
    """Retourne le mois de la date de fin la plus récente"""
    return getLastDate().month

def getLastDateDay():
    """Retourne le jour de la date de fin la plus récente"""
    return getLastDate().day


# ========== GESTION DES MOTS-CLES ==========

def getAllKeywords():
    """
    Extrait tous les mots-clés uniques de tous les projets CORDIS
    
    Returns:
        set: Ensemble des mots-clés conversis en minuscules et nettoyés
    """
    names = []

    for p in data.values():
        temp = p.get("project", {}).get("keywords")
        
        if temp:
            temp = temp.split(", ")
            
            for word in temp:
                names.append(word.lower())
    

    # Suppression des espaces au début et à la fin
    res = []
    for word in names:
        newWord = word

        if word[0] == ' ':
            newWord = newWord[1:]
        if word[-1] == ' ':
            newWord = newWord[:-1]
            
        res.append(newWord)
    return set(res)


# ========== RECHERCHE DE PROJETS ==========

def getAllProject(nomOrga):
    """
    Retourne la liste de tous les projets auxquels a participé une organisation donnée
    
    Parameters:
        nomOrga (str): Nom légal de l'organisation recherchée
    
    Returns:
        list: Liste de dictionnaires contenant:
            - title (str): Titre du projet
            - teaser (str): Accroche courte du projet
            - description (str): Description détaillée
            - date (str): Date de début au format 'YYYY-MM-DD'
            - cout (str): Coût total avec symbole €
            - allContributors (list): Liste des organisations collaboratrices
    """
    listeProjects = []

    for p in data.values():
        for orga in p["project"]["relations"]["associations"]["organization"]:
            if isinstance(orga, dict):
                if orga.get("legalName") == nomOrga:
                    title = p["project"]["title"]
                    teaser = p["project"]["teaser"]
                    description = p["project"]["objective"]
                    date = p["project"]["startDate"]
                    total_cost = p["project"]["totalCost"] + "€"
                    
                    allContributors = getAllOrganizationsFrom1Project(p)

                    listeProjects.append({"title" : title, "teaser" : teaser, "description" : description, "date" : date, "cout" : total_cost, "allContributors" : allContributors})

    return listeProjects

