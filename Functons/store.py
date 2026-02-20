import psycopg2 
from psycopg2.extras import RealDictCursor
import random
import logging
def addStore(conn,name,location,status='open'):
    """adds a store to the store table"""
    cursor=None
    try:
        if name is None or location is None or status is None:
            logging.error("name and location are required.")
            return False
        
        cursor = conn.cursor()
        name=str(name).strip()
        location=str(location).strip()
        status=str(status).strip().lower()

        if  status not in ['open','closed','maintenance']:
            logging.error(f"{status} is not a valid status")
            return False
        
        # Check if store with same name exists
        cursor.execute("SELECT 1 FROM stores WHERE name=%s;", (name,))
        row=cursor.fetchone()
        if row is not None:
            logging.info("store already exists")
            return None

        # Generate unique store_code
        startcode=f"{name[:3].upper()}"
        storecode=f"{startcode}-{random.randint(100,999)}"
        while True:
            cursor.execute("SELECT 1 FROM stores WHERE store_code=%s;", (storecode,))
            if cursor.fetchone() is None:
                break
            storecode=f"{startcode}-{random.randint(100,999)}"

        cursor.execute("INSERT INTO stores (name,location,status,store_code) VALUES (%s,%s,%s,%s) RETURNING store_id",(name,location,status,storecode))
        conn.commit()
        return cursor.fetchone()[0] # Return the new store's ID
    
    except psycopg2.IntegrityError:
        logging.info(f"{storecode} already exists")
        return None
    except psycopg2.Error as e:
        logging.exception(f"data error store.py: {e}")
        return False
    finally:
        cursor.close()

def getStoreByID(conn,store_id):
    cursor=None
    try:
        store_id=int(store_id)

        cursor=conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM stores WHERE store_id=%s",(store_id,))
        
        store=cursor.fetchone()
        if store is None:
            logging.warning("no Store found with store_id")
            return None
        
        return store
    
    except psycopg2.Error as e:
        logging.exception(f"Error in store.py: get_stor_by_ID {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("store_id must be an integer")
        return False
    finally:
        if cursor is not None:
            cursor.close()

#not tested
def update_store_status(conn,store_id,status):
    try:
        store_id=int(store_id)
        status=str(status).lower().strip()

        if status not in ["open", "closed","maintenance"]:
            logging.error(f"{status} is not a valid status type")
            return False
        
        # Check if store exists
        store_info=getStoreByID(conn,store_id)
        if not store_info:
            logging.error("store not found in database will not update store status")
            return False  
        elif store_info['status'] == status:
            logging.info("store already has the specified status")
            return True

        #update store status
        with conn.cursor() as cursor:
            cursor.execute("UPDATE stores SET status =%s WHERE store_id=%s",(status,store_id))

            conn.commit()
            return True
    
    except psycopg2.Error as e:
        logging.exception(f"data Error in store.py update_store_status {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("store_id must be an integer and status must be a string")
        return False
       
def get_store_by_store_code(conn,store_code):
    
    cursor=None
    try:

        store_code=str(store_code).strip()

        cursor=conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM stores WHERE store_code=%s",(store_code,))
        
        store=cursor.fetchone()
        if store is None:
            logging.warning("no Store found with store_code")
        
        return store
    
    except psycopg2.Error as e:
        logging.exception(f"Error in store.py: get_store_by_store_code {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("store_code must be a string")
        return False
    finally:
        if cursor is not None:
            cursor.close()

