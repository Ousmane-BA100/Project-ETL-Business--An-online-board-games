# ETL Pipeline pour une Plateforme de Jeux de Société en Ligne

Ce projet implémente un pipeline ETL (Extract, Transform, Load) pour analyser les données des joueurs d'une plateforme de jeux de société en ligne.

## Fonctionnalités

- **Extraction** des données de base et avancées des joueurs
- **Transformation** des données pour l'analyse
- **Chargement** dans une base de données PostgreSQL
- **Orchestration** avec Apache Airflow
- **Visualisation** via pgAdmin

## Architecture

project/
├── dags/                    # DAGs Airflow
│   └── etl_players.py       # DAG principal
├── scripts/                 # Scripts ETL
│   ├── extract_basic.py     # Extraction des données de base
│   ├── extract_advanced.py  # Extraction des données avancées
│   ├── transform.py         # Transformation des données
│   └── load_postgres.py     # Chargement dans PostgreSQL
├── sql/
│   └── init_tables.sql      # Schéma de la base de données
├── docker-compose.yml       # Configuration Docker
└── requirements.txt         # Dépendances Python

## Installation avec Docker

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Ousmane-BA100/Project-ETL-Business--An-online-board-games.git
   cd Project-ETL-Business--An-online-board-games
   ```

2. Lancez les services avec Docker Compose :
   ```bash
   docker-compose up -d
   ```

3. Accédez aux interfaces :
   - **Airflow** : http://localhost:8080 (admin/admin)
   - **pgAdmin** : http://localhost:5050 (admin@admin.com/admin)

## Flux de données

1. **Extraction** :
   - Données de base des joueurs
   - Statistiques avancées de jeu

2. **Transformation** :
   - Nettoyage des emails
   - Calcul du temps de jeu
   - Conversion des taux de victoire
   - Calcul de l'ancienneté

3. **Chargement** :
   - Stockage dans PostgreSQL
   - Tables optimisées pour l'analyse

## Tables de données

- `players_basic_raw` : Données brutes de base
- `players_adv_raw` : Statistiques avancées
- `players_clean` : Données transformées et nettoyées

## Exemples de requêtes

```sql
-- Joueurs les plus actifs
SELECT player_name, hours_of_play_last_month 
FROM players_clean 
ORDER BY hours_of_play_last_month DESC 
LIMIT 10;

-- Taux de victoire par jeu
SELECT 
    favorite_game, 
    ROUND(AVG(winrate_pct), 2) as avg_winrate
FROM players_clean
GROUP BY favorite_game
ORDER BY avg_winrate DESC;
```

## Développement

### Prérequis
- Docker et Docker Compose
- Python 3.7+

### Variables d'environnement

Créez un fichier `.env` à la racine :
```
AIRFLOW_UID=1000
AIRFLOW_GID=0
```

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Remerciements

- Apache Airflow pour l'orchestration
- PostgreSQL pour le stockage des données
- Pandas pour le traitement des données
