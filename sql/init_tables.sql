CREATE TABLE IF NOT EXISTS players_basic_raw (
    player_name TEXT,
    email TEXT,
    subscription_date TEXT,
    last_connexion_date TEXT
);

CREATE TABLE IF NOT EXISTS players_adv_raw (
    player_name TEXT,
    hours_of_play_last_month INT,
    favorite_game TEXT,
    items_bought TEXT,
    winrate TEXT
);

CREATE TABLE IF NOT EXISTS players_clean (
    player_name TEXT,
    email_clean TEXT,
    subscription_date DATE,
    last_connexion_date DATE,
    hours_of_play_last_month INT,
    favorite_game TEXT,
    items_bought_list TEXT,
    winrate_pct FLOAT,
    tenure_days INT,
    days_since_last_connexion INT,
    is_active_30d BOOLEAN
);
