import json

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

listeContributeurs = getListContributors("UNIVERSITE DU MANS")

for orga in listeContributeurs:
    print(getLocFromName(orga))