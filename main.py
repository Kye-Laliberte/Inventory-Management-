from operator import add
from webbrowser import get

from setup import setup
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from Functons.getTable import getTable as gt
from Functons.customers import getCustumerByID, addCustomer, UpdateCustomerInfo
from Functons.item import getItemByID, get_ItemBy_item_code, additem, updateItemInfo, updateItemStatus
from Functons.store import getStoreByID, get_store_by_store_code,update_store_status ,addStore

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
        UpdateCustomerInfo(conn,1,status="active")
        custumers=gt(conn,tables[5])
        
        # lists all customers
        for cust in custumers:
            print(f"item details: {cust}")
        
        

       
         # Seed data for categorys
        
    except psycopg2.Error as e:
        logging.exception(f"data error main.py: {e}")
    finally:
        if conn is not None:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
