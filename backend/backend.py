from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import scanR
import cordis

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


# requette qui renvoie tous les points gps des organisations ayant colloborées dans un projet inclus dans le dates passées en param
@app.get("/cordis/getAllLocalizationsFromDates")
def getAllLocalizationsFromDates(deb: str, fin: str):
    return cordis.getAllLocalizationsFromDates(deb, fin)