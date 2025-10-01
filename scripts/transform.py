import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def run():
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres/players_db")

    df_basic = pd.read_sql("SELECT * FROM players_basic_raw", engine)
    df_adv = pd.read_sql("SELECT * FROM players_adv_raw", engine)

    # Nettoyage email
    df_basic["email_clean"] = df_basic["email"].str.strip().str.lower()
    df_basic.loc[~df_basic["email_clean"].str.contains("@", na=False), "email_clean"] = np.nan

    # Dates
    df_basic["subscription_date"] = pd.to_datetime(df_basic["subscription_date"], errors="coerce")
    df_basic["last_connexion_date"] = pd.to_datetime(df_basic["last_connexion_date"], errors="coerce")

    # Winrate : gérer les None/vides avant conversion
    df_adv["winrate_clean"] = (
        df_adv["winrate"]
        .replace(["None", "none", "", "NaN"], np.nan)   # uniformiser
        .astype(str)
        .str.replace(",", ".", regex=False)             # remplacer la virgule par point
    )

    # convertir en float de manière sécurisée
    df_adv["winrate_clean"] = pd.to_numeric(df_adv["winrate_clean"], errors="coerce")

    # normaliser en %
    df_adv["winrate_pct"] = df_adv["winrate_clean"].apply(
        lambda x: x*100 if pd.notnull(x) and 0 <= x <= 1 else x if pd.notnull(x) and 0 < x <= 100 else np.nan
    )

    # Join
    df_final = df_basic.merge(df_adv, on="player_name", how="left")

    today = pd.Timestamp.today()
    df_final["tenure_days"] = (today - df_final["subscription_date"]).dt.days
    df_final["days_since_last_connexion"] = (today - df_final["last_connexion_date"]).dt.days
    df_final["is_active_30d"] = df_final["days_since_last_connexion"] <= 30

    # Sauvegarde
    df_final.to_sql("players_clean", engine, if_exists="replace", index=False)
    print("✅ Transform done")
