
"""

import requests

search = "https://api.archives-ouvertes.fr/search/?q=le mans&fl=*&wt=json"
labos = "https://api.archives-ouvertes.fr/ref/structure/"

def get_structures(query="*:*", rows=100):
    params = {
        "q": query,
        "rows": rows,
        "wt": "json"
    }

    response = requests.get(search, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception("Erreur lors de l'appel à l'API HAL")

    return response.json()["response"]["docs"]


def get_labo(id=0, rows=1):
    params = {
        "q": f"docid:{id} OR aliasDocid_i:{id}",
        "rows": rows,
        "wt": "json"
    }

    response = requests.get(labos, params=params, timeout=10)

    if response.status_code == 200:
        return response.json()["response"]["docs"]
    return []

name = ""
typestruct = ""
add = ""
def display_structures(structures):
    print("Structures trouvées :\n")

    for struct in structures:
        docid = struct.get("docid", "N/A")
        name = struct.get("label_s", "Nom inconnu")
        struct_id = struct.get("structId_i", "ID inconnu") # lmu
        add = struct.get("structAddress_s", "Adresse inconnue")
        pays = struct.get("structCountry_s", "Pays inconnu")
        #typestruct = struct.get("structType_s", "Type inconnu")
        accronyme = struct.get("structAcronym_s", "Acronyme inconnu")
        idlabo = struct.get("labStructId_i", "Laboratoire inconnu") #lium etc
        #adrlabo = struct.get("labStructAddress_s", "Adresse du labo inconnue")
        #colcode = struct.get("collCode_s", "Collaboration inconnue")
        #colCat = struct.get("collCategory_s", "Catégorie de collaboration inconnue")        
        col_codes = struct.get("collCode_s", [])
        col_cats = struct.get("collCategory_s", [])

        #if isinstance(idlabo, int):
        #    idlabo = [idlabo]
        #if isinstance(adrlabo, str):
        #    adrlabo = [adrlabo]
        


        if isinstance(col_codes, str):
            col_codes = [col_codes]
        if isinstance(col_cats, str):
            col_cats = [col_cats]
        coll_dict = dict(zip(col_codes, col_cats))



        #print(f"\n- {name} (id : {docid}) (structid : {struct_id}) (addresse: {list(set(add))}) (pays: {list(set(pays))}) (type: {typestruct}) (accronyme : {list(set(accronyme))} ) laboid : {idlabo}) (adresse labo : {adrlabo}) (collcode : {d})")
        #print(f"\n- {name} \n(id : {docid}) \n(structid : {struct_id}) \n(addresse: {list(set(add))}) \n(pays: {list(set(pays))}) \n(accronyme : {list(set(accronyme))} ) \nlaboid : {idlabo}) \n(adresse labo : {adrlabo}) \n(collcode : {d})")
        print(f"\n\n- {name} (structid : {struct_id}, docid : {docid})")
        print(f"  Adresse structure : {list(set(add))}")
        print(f"  Pays : {list(set(pays))}")
        print(f"  Acronyme : {list(set(accronyme))}")
        
        
        #affiche tjs le manus université
        #print(f"  Laboratoires :")
        #for lid, laddr in zip(idlabo, adrlabo):
        #    print(f"    - ID labo : {lid}, Adresse labo : {laddr}")
        print(f" id labo : {idlabo}")
        if(idlabo != "Laboratoire inconnu"):
            print(get_labo(idlabo[0]))
        
        
        #print(f"  Collaboration : {coll_dict}")

def main():
    recherches = get_structures(rows=15)
    display_structures(recherches)



if __name__ == "__main__":
    main()
"""




import requests
import time

# URLs d'origine
search = "https://api.archives-ouvertes.fr/search/?q=le mans&fl=*&wt=json"
labos = "https://api.archives-ouvertes.fr/ref/structure/"

def get_coordinates(adresse):
    """Récupère lat/lon à partir d'une adresse via l'API adresse.data.gouv.fr"""
    url_geo = "https://api-adresse.data.gouv.fr/search/"
    params = {"q": adresse, "limit": 1}
    try:
        # Petite pause pour respecter l'API si tu fais beaucoup de requêtes
        response = requests.get(url_geo, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['features']:
                # coordinates est [longitude, latitude]
                coords = data['features'][0]['geometry']['coordinates']
                return coords[1], coords[0] # On retourne (lat, lon)
    except Exception as e:
        print(f"  [!] Erreur géocodage : {e}")
    return None, None

def get_structures(query="*:*", rows=100):
    params = {
        "q": query,
        "rows": rows,
        "wt": "json"
    }
    response = requests.get(search, params=params, timeout=10)
    if response.status_code != 200:
        raise Exception("Erreur lors de l'appel à l'API HAL")
    
    data = response.json()
    return data.get("response", {}).get("docs", [])

def display_structures(structures):
    print("Structures trouvées (filtrées Mans avec Coordonnées) :\n")

    for struct in structures:
        name = struct.get("label_s", "Nom inconnu")
        address_list = struct.get("structAddress_s", [])
        
        # On transforme la liste en chaîne pour le filtrage et l'API
        if isinstance(address_list, list) and len(address_list) > 0:
            address_str = address_list[0] # On prend la première adresse de la liste
        else:
            address_str = str(address_list)
        
        # Filtrage : si "mans" est dans l'adresse
        if "mans" in address_str.lower():
            struct_id = struct.get("structId_i", "ID inconnu")
            accronyme = struct.get("structAcronym_s", "Acronyme inconnu")

            print(f"\n- {name}")
            print(f"  Adresse : {address_str}")
            
            # RÉCUPÉRATION DES COORDONNÉES
            lat, lon = get_coordinates(address_str)
            
            if lat and lon:
                print(f"  📍 GPS -> Latitude: {lat}, Longitude: {lon}")
            else:
                print(f"  📍 GPS -> Non trouvé")
                
            print(f"  Acronyme : {accronyme}")

def main():
    # On augmente le nombre de lignes pour avoir plus de résultats
    recherches = get_structures(query="le mans", rows=100)
    display_structures(recherches)

if __name__ == "__main__":
    main()