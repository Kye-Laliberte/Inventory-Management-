from setup import setup
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from Functons.getTable import getTable as gt
from Functons.customers import getCustumerByID
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

        dict=getCustumerByID(conn,3)
        #shows status of dict
        if dict is not None:
            logging.info(f"Customer details: {dict}")
        else:
            logging.info("Customer not found or an error occurred.")
        
        #shows thecustamer status of dict
        if dict is not None and 'status' in dict:
            logging.info(f"Customer status: {dict['status']}")
        
        dicts=getItemByID(conn,2)
        if dicts is not None:
            logging.info(f"Item details: {dicts}")
            logging.info(f"Item name: {dicts.get('name', 'N/A')}")
        else:
            logging.info("Item not found or an error occurred.")
        
        dictss=getStoreByID(conn,1)
        if dictss is not None:
            logging.info(f"Store details: {dictss}")
            logging.info(f"Store name: {dictss.get('name', 'N/A')}")



         # Seed data for categorys
    

        #purchaseslist=gt(conn,"purchases")
        #for pu in purchaseslist:
        #        logging.info(pu)

        #s I Q
        
    except psycopg2.Error as e:
        logging.exception(f"data error main.py: {e}")
    finally:
        if conn is not None:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
