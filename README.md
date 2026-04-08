# CCLMU - Collaborations de Le Mans Universités

## 📋 À propos du projet

**CCLMU** est une application web interactive de visualisation des collaborations scientifiques au Mans. Elle permet d'explorer les projets de recherche sourcés depuis deux bases de données majeures :

- **CORDIS** : Community Research and Development Information Service (Projets de recherche européens)
- **HAL** : Hyper Articles en Ligne (Publications scientifiques françaises)

L'application affiche les organisations et leurs collaborations sur une carte interactive, en filtrant par dates et mots-clés.

---

## 🎯 Objectifs

- Visualiser les organisations de recherche au Mans et leurs collaborations
- Afficher les projets CORDIS (subventions européennes)
- Lister les publications HAL (archives ouvertes scientifiques)
- Filtrer les données par plage de dates et mots-clés
- Présenter les informations de manière interactive et intuitive


---

## 🚀 Installation et configuration


### 2️⃣ Installation du Backend (Python)

```bash
# Créer l'environnement virtuel Python
cd backend
python3 -m venv backend_venv

# Activer l'environnement virtuel
source backend_venv/bin/activate  # Linux/Mac
# OU
.\backend_venv\Scripts\activate   # Windows

# Installer les dépendances Python
pip install fastapi uvicorn requests python-dotenv
```

### 3️⃣ Configuration d'authentification (ScanR - optionnel)

Certaines fonctionnalités nécessitent des identifiants :

```bash
# Créer le fichier .private_env à la racine ou dans backend/
touch .private_env

# Ajouter vos identifiants
echo "SCANR_USERNAME=votre_username" >> .private_env
echo "SCANR_PASSWORD=votre_password" >> .private_env
```

---

## 🎮 Utilisation

### Lancer l'application (local)

#### Terminal 1 - Frontend Angular

```bash
ng serve
```

L'application est accessible à : **http://localhost:8080**

#### Terminal 2 - Backend FastAPI

```bash
cd backend
source backend_venv/bin/activate  # Activer l'environnement

# Lancer le serveur FastAPI
python -m uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

L'API est accessible à : **http://localhost:8000**
Documentation Swagger : **http://localhost:8000/docs**

---

## 📡 API Endpoints

### Endpoints CORDIS

| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|-----------|
| GET | `/cordis/firstDate` | Date de début la plus ancienne | - |
| GET | `/cordis/lastDate` | Date de fin la plus récente | - |
| GET | `/cordis/firstDate/{year\|month\|day}` | Composante de date de début | - |
| GET | `/cordis/lastDate/{year\|month\|day}` | Composante de date de fin | - |
| GET | `/cordis/getAllLocalizationsFromDates` | Localisations filtrées | `deb`, `fin`, `keywords` |
| GET | `/cordis/listOfProject` | Projets d'une organisation | `nomOrga` |

### Endpoints HAL

| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|-----------|
| GET | `/hal/firstDate/{year\|month}` | Date de première publication | - |
| GET | `/hal/getCoordinatesFromDates` | Coordonnées GPS filtrées | `anneeMin`, `anneeMax`, `moisMin`, `moisMax` |
| GET | `/hal/getDataFromFilters` | Publications filtrées | `anneeMin`, `anneeMax`, `moisMin`, `moisMax`, `keywords` |
| GET | `/hal/getProjectsFromCollab` | Collaborations HAL | `nomOrga`, `limite` |

---


## 👥 Contributeurs

- **Développeurs** : Ilann Thourault / Lucas Reverbel--Longhi / Nathan Morin
- **Année académique** : L3
- **Institution** : Le Mans Université

---