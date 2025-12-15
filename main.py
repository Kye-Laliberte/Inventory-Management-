import logging
import psycopg2
from Functons import purchases
from Functons import inventory
from Functons import store
from Functons import customers
from Functons import item
from Functons import getTable as gt
from setup import  setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
def main():

    conn=psycopg2.connect(dbname="datastore", user="postgres", password="132", host="localhost",port="13579")
        
    try:
        # Setup the database (create tables and seed data)
        #setup(conn, schema_path="Store.sql") # Connect to the database
        #logging.info("Database setup complete.")
        logging.info("Retrieving all customers:")
        
        customers_list = gt.getTable(conn, "stores")
        for customer in customers_list:
            logging.info(customer)

    except psycopg2.Error as e:
        logging.exception(f"data error main.py: {e}")
    finally:
        if conn is not None:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
#services.msc
#PostgreSQL cmd 
#Windows + R for command prompt
#"C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" start -D "C:\Program Files\PostgreSQL\17\data"
#server start

#server stop
# "C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" stop -D "C:\Program Files\PostgreSQL\17\data"

#psql -U postgres -h localhost -p 13543

#password: 132
#port: 13579