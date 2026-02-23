from webbrowser import get

from setup import setup
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from Functons.getTable import getTable as gt
from Functons.customers import getCustumerByID, addCustomer
from Functons.item import getItemByID
from Functons.store import getStoreByID 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
def main():

    conn=psycopg2.connect(dbname="datastore", user="postgres", password="12345", host="localhost",port="5433")
        #ps 1-5
    try:
        #Setup the database (create tables and seed data)
        #setup.setup(conn) 
        # # Connect to the database
        #logging.info("Database setup complete.")
        
        tables=["purchases","stores","categorys","inventory","items","customers"]

        val=addCustomer(conn,"Greg Feay","123-5353","greg.feay@example.com",customer_tier=2,status='active')
        print(f"New customer ID: {val}")         
        custumers=gt(conn,tables[5])
        
        # lists all customers
        for cust in custumers:
            logging.info(f"Customer details: {cust}")
        
        logging.info(f"Item details: {dict}")


         # Seed data for categorys
        
    except psycopg2.Error as e:
        logging.exception(f"data error main.py: {e}")
    finally:
        if conn is not None:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
