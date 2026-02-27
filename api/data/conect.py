import os

import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path("C:/projects/vs stuff 2/New folder (2)/Inventory-Management-/api/.env")
load_dotenv(dotenv_path=dotenv_path)

@contextmanager
def get_connection():

    print(os.getenv("DB_USER"))
    print(os.getenv("DB_PASSWORD"))
    print(os.getenv("DB_HOST"))
    print(os.getenv("DB_PORT"))
    print(os.getenv("DB_NAME"))

    conn= psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
        )
    

    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()

    
        #uvicorn api.main:app --reload
        
    
         # Seed data for categorys
        