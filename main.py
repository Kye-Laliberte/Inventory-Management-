import logging
import psycopg2
from Functons import inventory
from Functons import store
from Functons import customers
from setup import setup


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
def main():
    # Setup the database (create tables and seed data)
    
    setup()# Connect to the database
    logging.info("Database setup complete.")
    
    conn = psycopg2.connect(
        dbname="datastore",user="postgres",password="your_password",host="localhost",port="5432")