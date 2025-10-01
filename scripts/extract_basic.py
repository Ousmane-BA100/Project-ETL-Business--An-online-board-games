import requests
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine

BASE_URL = "https://players.data.polyprojects.fr"

def run():
    r = requests.get(f"{BASE_URL}/basic_player_data", timeout=30)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text), sep="|")

    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres/players_db")
    df.to_sql("players_basic_raw", engine, if_exists="replace", index=False)
    print("✅ Extract basic done")
