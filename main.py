from operator import add
from webbrowser import get
from dotenv import load_dotenv
import os
from setup import setup
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from Functons.getTable import getTable as gt
from Functons.customers import getCustumerByID, addCustomer, UpdateCustomerInfo
from Functons.item import getItemByID, get_ItemBy_item_code, additem, updateItemInfo, updateItemStatus
from Functons.store import getStoreByID, get_store_by_store_code,update_store_status ,addStore
from Functons.inventory import UpdateToInventory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
def main():

    load_dotenv()

    conn = psycopg2.connect(
        dbname=os.getenv("dbname"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port")) 

    try:
        #Setup the database (create tables and seed data)
        #setup.setup(conn) 
        # # Connect to the database
        #logging.info("Database setup complete.")
        
        tables=["purchases","stores","categorys","inventory","items","customers"]
        
        custumers=gt(conn,tables[4])
        
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
