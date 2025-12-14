import psycopg2 
import random
import logging
def addstore(conn,name,location,status='open'):
    """adds a store to the store table"""
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