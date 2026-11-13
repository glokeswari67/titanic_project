import os
import psycopg2
import pandas as pd

def get_connection(read_only=False):
    connection = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "titanic_db"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", ""),
        options="-c search_path=titanic_project,public"
    )
    if read_only:
        connection.set_session(readonly=True, autocommit=True)
    return connection

def read_sql(query, params=None):
    connection = get_connection(read_only=True)
    try:
        return pd.read_sql_query(query, connection, params=params)
    finally:
        connection.close()
