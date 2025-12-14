import psycopg2 
import random
import logging
def addstore(conn,name,location,status='open'):
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

def get_store_status(conn,store_id):
    """retrieves the status of a store by its ID"""
    cursor=None
    try:
        cursor=conn.cursor()
        cursor.execute("SELECT status FROM stores WHERE store_id=%s",(store_id,))
        store_status = cursor.fetchone()
        
        if store_status is None:
            logging.error("store not found")
            return None
        return store_status[0]
    except psycopg2.Error as e:

        logging.exception(f"data error store.py: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()

