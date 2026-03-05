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
def getFirtDate():
    return cordis.getFirstDateYear()
@app.get("/cordis/firstDate/month")
def getFirtDate():
    return cordis.getFirstDateMonth()
@app.get("/cordis/firstDate/day")
def getFirtDate():
    return cordis.getFirstDateDay()



@app.get("/cordis/lastDate")
def getLastDate():
    return cordis.getLastDate()

@app.get("/cordis/lastDate/year")
def getFirtDate():
    return cordis.getLastDateYear()
@app.get("/cordis/lastDate/month")
def getFirtDate():
    return cordis.getLastDateMonth()
@app.get("/cordis/lastDate/day")
def getFirtDate():
    return cordis.getLastDateDay()