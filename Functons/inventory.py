import psycopg2
import logging
import datetime as dtime
from psycopg2.extras import RealDictCursor
from Functons.item import getItemByID
from Functons.store import getStoreByID
def UpdateToInventory(conn,store_id,item_id,newquantity,status='active'):
    """
    Updates the inventory quantity or adds a new inventory record.
    Parameters:
        conn: psycopg2 connection object to the database.
        store_id int: The ID of the store.
        item_id int: The ID of the item.
        newquantity int: The new quantity to set.
        status (str, optional): The status of the inventory item (default is 'active').
    Returns:
        int: The new inventory's ID if a new record is inserted.
        True: If the inventory was updated successfully or quantity already matches.
        False: If an error occurs or input is invalid.
        None: If the store or item is not found.
    """
    if store_id is None or item_id is None or newquantity is None:
        logging.error("store_id, item_id, and newquantity are required.")
        return False
    try:
        store_id=int(store_id)
        item_id=int(item_id)
        newquantity=int(newquantity)
        status=str(status).strip().lower()
    except (ValueError, TypeError):
        logging.exception("store_id, item_id, and newquantity must be integers")
        return False
    
    if newquantity<0:
        logging.error("quantity cannot be negative")
        return False
    cursor=None
    try:

        cursor=conn.cursor()
        """
        cursor.execute("SELECT status FROM stores WHERE store_id=%s",(store_id,))
        store_status = cursor.fetchone()
        if store_status is None:
            logging.error("store not found")
            return False
        cursor.execute("SELECT status FROM items WHERE item_id=%s",(item_id,))
        item_status = cursor.fetchone()
        if item_status is None:
            logging.error("item not found")
            return False
        
        if store_status[0] != 'open':
            logging.warning("store %s is not open",store_id)
            return False
        if item_status[0] != 'active':
            logging.warning("item %s is not active",item_id)
            return False
        """ 
        
        item=getItemByID(conn,item_id)
        if item is None:
            logging.error("item not found in database will not update inventory")
            return False
        elif 'status' not in item:
            logging.error("item status not found in database will not update inventory")
            return False
        elif item.get('status') != 'active':
            logging.warning("item %s is not active",item_id)
            return False
        
        store_info=getStoreByID(conn,store_id)
        if store_info is None:
            logging.error("store not found in database will not update inventory")
            return False
        elif 'status' not in store_info:
            logging.error("store status not found in database will not update inventory")
            return False
        elif store_info['status'] != 'open':
            logging.warning("store %s is not open",store_id)
            return False

        cursor.execute("SELECT quantity FROM inventory WHERE store_id=%s AND item_id=%s",(store_id,item_id))
        row=cursor.fetchone()
        
        if (row):
            quantity=int(row[0])
            if(quantity==newquantity):
                logging.info("quantity already matches")
                return True
            
            if newquantity==0:
                status='inactive'
            
            cursor.execute("""UPDATE inventory
                           SET quantity=%s,status=%s
                           WHERE store_id = %s AND item_id = %s""",(newquantity,status,store_id,item_id))
            conn.commit()
            return True

        else:  
            cursor.execute("""INSERT INTO inventory (store_id,item_id,quantity,status)  
                       VALUES (%s,%s,%s,%s)""" ,(store_id,item_id,newquantity,status))
            conn.commit()
        result=cursor.fetchone()
        return True
    
    except psycopg2.Error as e:
        logging.exception(f"data error inventory.py")
        return False
    finally:
        if cursor is not None:
            cursor.close()

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
