import json
import datetime

# Chargement du json en global
with open("ressources/publications.json", "r", encoding="utf-8") as f:
    data = json.load(f)


# Récupère un projet en fonction de son id
def getProjectFromId(id: int):
    id_str = str(id)
    return data.get(id_str)

# Retourne la liste des noms des organisation qui ont leur adresse au Mans
def getAllLeMansOrganizations():
    names = []

    for p in data.values():
        for orga in p["project"]["relations"]["associations"]["organization"]:
            if isinstance(orga, dict):  # on vérifie que c'est bien un dictionnaire
                if orga.get("address").get("city") == "Le Mans":
                    names.append(orga["legalName"])
    
    unique_names = list(set(names))
    return unique_names

# Retourne la liste de toutes les adresses des organisations
def getAllLocalizations():
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
    loc = []

    for orga in project["project"]["relations"]["associations"]["organization"]:
        if isinstance(orga, dict):
            geo = orga.get("address").get("geolocation")
            if geo:
                loc.append(geo)
    
    unique_loc = list(set(loc))
    return unique_loc

def createDateFromStr(dateStr):
    year = int(dateStr[0:4]) 
    month = int(dateStr[5:7])
    day = int(dateStr[8:10])
    return datetime.date(year, month, day)

def getAllLocalizationsFromDates(dateDebStr, dateFinStr):
    loc = []

    dateDeb = createDateFromStr(dateDebStr)
    dateFin = createDateFromStr(dateFinStr)

    for p in data.values():

        project = p["project"]

        dateDebTemp = createDateFromStr(project["startDate"])
        dateFinTemp = createDateFromStr(project["endDate"])

        if (dateDebTemp > dateDeb and dateDebTemp < dateFin) or \
           (dateFinTemp > dateDeb and dateFinTemp < dateFin):

            loc.extend(getAllLocalizationsFrom1Project(p))

    return list(set(loc))
            


##### Liste des orgas du Mans

#METACOUSTIC
#Centre Hospitalier Le Mans
#SILENTSYS
#ACO AUTOMOBILE CLUB DE L'OUEST
#GUATECS
#COMMUNAUTE URBAINE DE LE MANS METROPOLE
#UNIVERSITE DU MANS

# Fonction privée, est réutilisée dans getListContributors
def getListContributors1Project(projet, nomOrga: str):
    listContributors = []

    for orga in projet["project"]["relations"]["associations"]["organization"]:
        if isinstance(orga, dict):
            if orga.get("legalName") != nomOrga:
                listContributors.append(orga.get("legalName"))

    return listContributors

# Permet de renvoyer la liste de toute les collaborations de l'organisation passée en paramètres
def getListContributors(nomOrga: str):
    listContributors = []

    for p in data.values():
        for orga in p["project"]["relations"]["associations"]["organization"]:
            if isinstance(orga, dict):
                if orga.get("legalName") == nomOrga:
                    listContributors.extend(getListContributors1Project(p, nomOrga))

    
    unique_listContributors = list(set(listContributors))
    return unique_listContributors


def getLocFromName(nomOrga: str):

    for p in data.values():
        for orga in p["project"]["relations"]["associations"]["organization"]:
            if isinstance(orga, dict):
                if orga.get("legalName") == nomOrga:
                    return orga.get("address").get("geolocation")

    return "ERROR : Le nomOrga n'existe pas"
    

#print(getLocFromName("METACUSTIC"))
#print(getLocFromName("Centre Hospitalier Le Mans"))
#print(getLocFromName("SILENTSYS"))
#print(getLocFromName("ACO AUTOMOBILE CLUB DE L'OUEST"))
#print(getLocFromName("GUATECS"))
#print(getLocFromName("COMMUNAUTE URBAINE DE LE MANS METROPOLE")) ne pas utiliser pour le moment car adresse a mont de marsan
#print(getLocFromName("UNIVERSITE DU MANS"))

def getFirtDate():
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
    return getFirtDate().year
def getFirstDateMonth():
    return getFirtDate().month
def getFirstDateDay():
    return getFirtDate().day


def getLastDate():
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
    return getLastDate().year
def getLastDateMonth():
    return getLastDate().month
def getLastDateDay():
    return getLastDate().day




listeContributeurs = getListContributors("UNIVERSITE DU MANS")
'''
print(getFirtDate())
print(getFirstDateYear())
print(getFirstDateMonth())
print(getFirstDateDay())
print(getLastDate())
print(getLastDateYear())
print(getLastDateMonth())
print(getLastDateDay())
'''

for i in getAllLocalizationsFromDates("2016-09-01", "2019-09-01"):
    print(i)

#for orga in listeContributeurs:
 #   print(getLocFromName(orga))