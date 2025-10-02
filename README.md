# ETL Pipeline pour une Plateforme de Jeux de Société en Ligne

Ce projet implémente un pipeline ETL (Extract, Transform, Load) pour analyser les données des joueurs d'une plateforme de jeux de société en ligne.

## Fonctionnalités

- **Extraction** des données de base et avancées des joueurs
- **Transformation** des données pour l'analyse
- **Chargement** dans une base de données PostgreSQL
- **Orchestration** avec Apache Airflow
- **Visualisation** via pgAdmin

## Architecture
```
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
```
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
-- Voir les 10 premiers joueurs
SELECT * FROM players_clean LIMIT 10;

-- Nombre de joueurs par jeu favori
SELECT 
    favorite_game, 
    COUNT(*) as player_count,
    ROUND(AVG(winrate_pct)::numeric, 2) as avg_winrate
FROM players_clean
WHERE favorite_game IS NOT NULL
GROUP BY favorite_game
ORDER BY player_count DESC;

-- Joueurs actifs (connectés dans les 30 derniers jours)
SELECT 
    player_name,
    email_clean as email,
    days_since_last_connexion,
    winrate_pct
FROM players_clean
WHERE is_active_30d = true
ORDER BY winrate_pct DESC NULLS LAST;

-- Taux de victoire par jeu
SELECT 
    favorite_game, 
    ROUND(AVG(winrate_pct::numeric), 2) as avg_winrate
FROM players_clean
WHERE favorite_game IS NOT NULL
GROUP BY favorite_game
ORDER BY avg_winrate DESC NULLS LAST;

-- Version avec gestion des erreurs de conversion
WITH playtime_data AS (
    SELECT 
        player_name,
        winrate_pct,
        CASE 
            WHEN hours_of_play_last_month ~ '^[0-9]+$' THEN hours_of_play_last_month::integer
            ELSE NULL
        END as playtime_int
    FROM players_clean
)
SELECT 
    CASE 
        WHEN playtime_int IS NULL THEN 'Non renseigné ou invalide'
        WHEN playtime_int = 0 THEN '0h'
        WHEN playtime_int < 10 THEN '1-9h'
        WHEN playtime_int < 50 THEN '10-49h'
        ELSE '50h+'
    END as playtime_category,
    COUNT(*) as player_count,
    ROUND(AVG(winrate_pct)::numeric, 2) as avg_winrate
FROM playtime_data
GROUP BY playtime_category
ORDER BY player_count DESC;
```

## Développement

### Prérequis
- Docker et Docker Compose
- Python 3.7+

## Remerciements

- Apache Airflow pour l'orchestration
- PostgreSQL pour le stockage des données
- Pandas pour le traitement des données
