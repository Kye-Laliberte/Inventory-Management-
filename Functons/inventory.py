import psycopg2
import logging
import datetime as dtime
from psycopg2.extras import RealDictCursor
from Functons.item import getItemByID
from Functons.store import getStoreByID
import psycopg2.errors
from psycopg2.errors import ForeignKeyViolation
def UpdateToInventory(conn,store_id,item_id,newquantity=0,status='active'):
    """
    Updates the inventory quantity or adds a new inventory record.
    Parameters:
        conn: psycopg2 connection object to the database.
        store_id int: The ID of the store.
        item_id int: The ID of the item.
        newquantity int: The new quantity to set.
        status (str, optional): The status of the inventory item (default is 'active').
    """
    if store_id is None or item_id is None:
        logging.error("store_id and item_id are required.")
        return False
    try:
        store_id=int(store_id)
        item_id=int(item_id)
    
        newquantity=int(newquantity)
        status=str(status).strip().lower()
    except (ValueError, TypeError):
        logging.exception("store_id, item_id, and newquantity must be integers")
        return False
    
    if newquantity is not None and newquantity<0:
        logging.error("quantity cannot be negative")
        return False
    
    cursor=None
    try:

        with conn.cursor() as cursor:
            cursor.execute("SELECT quantity FROM inventory WHERE store_id=%s AND item_id=%s",(store_id,item_id))
            row=cursor.fetchone()

        #update existing inventory record if it exists
            if (row):
                quantity=int(row[0])
                
            
                if newquantity==0:
                    status='inactive'

                if(quantity==newquantity):
                    logging.info("quantity already matches")
                    return True
            
                cursor.execute("""UPDATE inventory
                            SET quantity=%s,status=%s
                            WHERE store_id = %s AND item_id = %s""",(newquantity,status,store_id,item_id))
                conn.commit()
                return True
        
        #create new inventory record if it does not exist
            else:  
                cursor.execute("""INSERT INTO inventory (store_id,item_id,quantity,status)  
                       VALUES (%s,%s,%s,%s)""" ,(store_id,item_id,newquantity,status))
                conn.commit()
            result=cursor.fetchone()
            return True
    
    except psycopg2.Error as e:
        logging.exception(f"data error inventory.py UpdateToInventory: {e}")
        return False
    except  ForeignKeyViolation as e:
        logging.exception(f"foreign key violation in inventory.py UpdateToInventory: {e}")
        return False
    
def get_inventory(conn,store_id,item_id):
    
    try:
        try:
            store_id=int(store_id)
            item_id=int(item_id)
        except (ValueError, TypeError):
            logging.exception("store_id and item_id must be integers")
            return False

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM inventory WHERE store_id=%s AND item_id=%s",(store_id,item_id))
        
            inventory=cursor.fetchone()
            if inventory is None:
                logging.warning("no inventory found for store_id and item_id")
                return None
        
            return inventory
    
    except psycopg2.Error as e:
        logging.exception(f"Error in inventory.py: get_inventory_by_store_and_item {e}")
        return False
    
def getInventoryByItem(conn,item_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            
            item_id=int(item_id)
            
            cursor.execute("SELECT * FROM inventory WHERE item_id=%s",(item_id,))
            
            inventory=cursor.fetchall()
            if not inventory:
                logging.warning("no inventory found for item_id")
                return False
            
            return inventory
        
        except psycopg2.Error as e:
            logging.exception(f"Error in inventory.py: get_inventory_by_item {e}")
            return False
        except (ValueError, TypeError):
            logging.exception("item_id must be an integer")
            return False
        
def getInventoryOfStore(conn,store_id):
    try:
        
        store_id=int(store_id)

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM inventory WHERE store_id=%s",(store_id,))
        
            inventory=cursor.fetchall()

        if not inventory:
            logging.warning("no inventory found for store_id")
            return False
        
        return inventory
    
    except psycopg2.Error as e:
        logging.exception(f"Error in inventory.py: get_inventory_by_store {e}")
        return False
    except (ValueError, TypeError):
            logging.exception("store_id must be an integer")
            return False
