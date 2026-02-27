import psycopg2 
from psycopg2.extras import RealDictCursor
import random
import logging
from ..data.conect import get_connection
def addStore(name:str,location:str,status:str='active'):
    """adds a store to the store table"""
    try:
        name=name.strip()
        location=location.strip()
        
        
        with get_connection() as conn:
            with conn.cursor() as cursor:

                # Generate unique store_code
                startcode=f"{name[:3].upper()}"
             
                while True:
                    storecode=f"{startcode}-{random.randint(100,999)}"
                    cursor.execute(
                        "SELECT 1 FROM stores WHERE store_code=%s;", (storecode,))
                    if cursor.fetchone() is None:
                        break

                cursor.execute("""
                               INSERT INTO stores (name,location,status,store_code) 
                               VALUES (%s,%s,%s,%s) 
                               RETURNING store_id""",(name,location,status,storecode))
                adedstore=cursor.fetchone()[0]# Return the new store's ID
                conn.commit()
                return  adedstore
    
    except psycopg2.IntegrityError as g:
        logging.info(f" IntegrityError {g}")
        return None
    except psycopg2.Error as e:
        logging.exception(f"data error store.py: {e}")
        return False
       
def getStoreByID(store_id: int):
    try:
        with get_connection() as conn:

            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM stores WHERE store_id=%s",
                               (store_id,))
                store=cursor.fetchone()
                
                if not store:
                    return None

            return store# None if no store
    
    except psycopg2.Error as e:
        logging.exception(f"Error in store.py: getStoreByID{e}")
        return False
    except (ValueError, TypeError):
        logging.exception("store_id must be an integer")
        return False

def UpdateStoreStatus(store_id:int,status: str):
    try:
        status=str(status).lower().strip()

        #update store status
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE stores SET status =%s WHERE store_id=%s",(status,store_id))

                conn.commit()

        return True
    except psycopg2.Error as e:
        logging.exception(f"data Error in store.py update_store_status {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("ValueError, TypeError")
        return False
    except Exception as e2:
        logging.exception(f"Error updating store status: {e2}")
        return False
def GetBystore_code(store_code):
    """Retrieves a store from the stores table based on the provided store_code.
    Returns a dictionary containing the store's details if found.,"""
    try:
        store_code=store_code.strip()
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM stores WHERE store_code=%s",(store_code,))
                store=cursor.fetchone()# none if not found

                if not store:
                    return None
      
        return store
    
    except psycopg2.Error as e:
        logging.exception(f"Error in store.py: get_store_by_store_code {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("store_code must be a string")
        return False
    

