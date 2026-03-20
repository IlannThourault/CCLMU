from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

import scanR
import cordis
import hal

app = FastAPI()

# Autoriser Angular (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Listening...")

@app.get("/scanR")
def get_markers():
    return scanR.get_markers()

@app.get("/cordis/firstDate")
def getFirtDate():
    return cordis.getFirtDate()

@app.get("/cordis/firstDate/year")
def getFirstDateYear():
    return cordis.getFirstDateYear()
@app.get("/cordis/firstDate/month")
def getFirstDateMonth():
    return cordis.getFirstDateMonth()
@app.get("/cordis/firstDate/day")
def getFirstDateDay():
    return cordis.getFirstDateDay()




############ CORDIS ###########
@app.get("/cordis/lastDate")
def getLastDate():
    return cordis.getLastDate()

@app.get("/cordis/lastDate/year")
def getLastDateYear():
    return cordis.getLastDateYear()
@app.get("/cordis/lastDate/month")
def getLastDateMonth():
    return cordis.getLastDateMonth()
@app.get("/cordis/lastDate/day")
def getLastDateDay():
    return cordis.getLastDateDay()


# requette qui renvoie tous les points gps des organisations ayant colloborées dans un projet inclus dans les dates passées en param (cordis)
@app.get("/cordis/getAllLocalizationsFromDates")
def getAllLocalizationsFromDates(deb: str, fin: str, keywords: str):
    return cordis.getAllLocalizationsFromDates(deb, fin, keywords)


@app.get("/cordis/listOfProject")
def getAllProject(nomOrga : str):
    return cordis.getAllProject(nomOrga)






#http://localhost:4200/hal/getCoordinatesFromDates?anneeMin=2000&anneeMax=2010&moisMin=1&moisMax=12

# requette qui renvoie tous les points gps des organisations ayant colloborées dans un projet inclus dans les dates passées en param (hal)
@app.get("/hal/getCoordinatesFromDates")
def getCoordinatesFromDates(anneeMin: int, anneeMax: int, moisMin: int, moisMax: int):
    return hal.getCoordinatesFromDates(anneeMin, anneeMax, moisMin, moisMax)


#http://localhost:4200/hal/getDataFromFilters?anneeMin=2000&anneeMax=2010&moisMin=1&moisMax=12&keywords=Le Mans
@app.get("/hal/getDataFromFilters")
def get_filtered_results(anneeMin: int, anneeMax: int, moisMin: int, moisMax: int, keywords: str = ""):
    if moisMin == 1:
        moisMin = 0  
    list_kw = [k.strip().lower() for k in keywords.split(",")] if keywords else []
    return hal.getDataFromFilters(anneeMin, anneeMax, moisMin, moisMax, list_kw)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content="", media_type="image/x-icon")