# CCLMU - Collaborations de Le Mans Universités
	
## À propos du projet

**CCLMU** est une application web interactive de visualisation des collaborations scientifiques au Mans. Elle permet d'explorer les projets de recherche sourcés depuis deux bases de données majeures :

- **CORDIS** : Community Research and Development Information Service (Projets de recherche européens)
- **HAL** : Hyper Articles en Ligne (Publications scientifiques françaises)

L'application affiche les organisations et leurs collaborations sur une carte interactive, en filtrant par dates et mots-clés.

---

## Objectifs

- Visualiser les organisations de recherche au Mans et leurs collaborations
- Afficher les projets CORDIS (subventions européennes)
- Lister les publications HAL (archives ouvertes scientifiques)
- Filtrer les données par plage de dates et mots-clés
- Présenter les informations de manière interactive et intuitive


---

## Installation et configuration

###  Configuration d'authentification avec ScanR

Certaines fonctionnalités nécessitent des identifiants :

```bash
# Dans .private_env
SCANR_USERNAME=votre_username
SCANR_PASSWORD=votre_password
```

---

## Utilisation

### Lancer l'application (local)

#### Backend Python

```bash
bash backend_launcher.sh
```

L'addresse de l'API serveur est inscrite dans .public_env.

#### Frontend Angular

```bash
npm start
```

---

## API Endpoints

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
