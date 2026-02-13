from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import scanR

app = FastAPI()

# Autoriser Angular (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Listening...")

@app.get("/scanR")
def get_markers():
    return scanR.get_markers()