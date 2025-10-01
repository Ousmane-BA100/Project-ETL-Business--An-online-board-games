# Pipeline ETL joueurs — Airflow + PostgreSQL

## Objectif
Mettre en place une pipeline automatisée pour :
- **Extraire** les données depuis les deux API (`/basic_player_data` et `/advanced_player_data_csv`).  
- **Transformer** les données (nettoyage, normalisation, calcul de features).  
- **Charger** le dataset final dans PostgreSQL.  
- **Orchestrer** l’ensemble avec Airflow.  

## Architecture

extract_basic --->
--> transform --> load_postgres
extract_advanced -->

## Étapes de la pipeline

### 1. Extraction
- **Task 1 — extract_basic** : appel `GET /basic_player_data`, sauvegarde en `basic.csv`.  
- **Task 2 — extract_advanced** : appel `GET /advanced_player_data_csv` (ou lecture du CSV enrichi déjà généré), sauvegarde en `advanced.csv`.  

### 2. Transformation
- **Task 3 — transform** :  
  - Lecture des deux CSV avec pandas.  
  - Nettoyage des emails, dates, winrate, parsing `items_bought`.  
  - Calcul des features (`tenure_days`, `days_since_last_connexion`, `is_active_30d`).  
  - Génération d’un `clean.csv` (dataset final).  

### 3. Load
- **Task 4 — load_postgres** :  
  - Insertion du dataset final dans PostgreSQL (table `players_clean`).  
  - Optionnel : conserver aussi les tables brutes (`players_basic_raw`, `players_adv_raw`).  

## Outils
- **Airflow** : orchestration des tasks (DAG).  
- **Python + pandas** : extraction et transformation.  
- **PostgreSQL** : stockage des données.  
- **Power BI** : reporting et visualisation.  

## Prochaines étapes
1. Créer un DAG Airflow avec 4 tasks (`extract_basic`, `extract_advanced`, `transform`, `load_postgres`).  
2. Conteneuriser l’environnement avec Docker Compose (`airflow + postgres + jupyter`).  
3. Connecter Power BI à la table `players_clean`.  
