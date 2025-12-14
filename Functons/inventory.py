import psycopg2
import logging


def addToInventory(conn,store_id,item_id,newquantity,status='active'):
    """
    Updates the inventory quantity or adds a new inventory record.

    Parameters:
        conn: psycopg2 connection object to the database.
        store_id (int): The ID of the store.
        item_id (int): The ID of the item.
        newquantity (int): The new quantity to set.
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
    store_id=int(store_id)
    item_id=int(item_id)
    newquantity=int(newquantity)
    status=str(status).strip().lower()

    if newquantity<0:
        logging.error("quantity cannot be negative")
        return False
    cursor=None
    try:

        cursor=conn.cursor()

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

        cursor.execute("SELECT quantity FROM inventory WHERE store_id=%s AND item_id=%s",(store_id,item_id))
        row=cursor.fetchone()
        
        if (row):
            quantity=row[0]
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
                       VALUES (%s,%s,%s,%s) RETURNING inventory_id""" ,(store_id,item_id,newquantity,status))
            conn.commit()
            return cursor.fetchone()[0] # Return the new inventory's ID

    except psycopg2.Error as e:
        logging.exception(f"data error inventory.py")
        return False
    finally:
        if cursor:
            cursor.close()
