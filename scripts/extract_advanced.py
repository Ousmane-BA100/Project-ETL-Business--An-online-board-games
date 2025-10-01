import pandas as pd
from sqlalchemy import create_engine

def run():
    # Lecture du fichier local
    df = pd.read_csv("/opt/airflow/scripts/players_upload_adv.csv")

    # Connexion à PostgreSQL
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres/players_db")

    # Écriture dans la table
    df.to_sql("players_adv_raw", engine, if_exists="replace", index=False)
    print("✅ Extract advanced (from local CSV) done")