import psycopg2
import logging
import datetime as dtime
from Functons.inventory import addToInventory
def addpurchase(conn,customers_id, item_id,store_id,quantity,purchases_date=None):
    """adds a purchase reaturns True if added False if error and none if sumthing is missing"""
    if quantity<=0:
        logging.error("at least 1 item must purchase at a time one item")
        return False
        
    cursor=None
    try:

        try:
            quantity=int(quantity)
            customers_id=int(customers_id)
            item_id=int(item_id)
            store_id=int(store_id)
        except ValueError:
            logging.error("incorect vareabal types")

        status='active'
        if customers_id is None or item_id is None or store_id is None or quantity is None:
            logging.error("customers_id, item_id, store_id, and quantity are required.")
            return False
        
        if not purchases_date:
            purchases_date=dtime.datetime.now().date()

        elif isinstance(purchases_date, str):
            try:
                purchases_date=dtime.datetime.strptime(purchases_date, "%Y-%m-%d").date()
            except ValueError:
                logging.error("purchases_date must be in YYYY-MM-DD format.")
                return False
            
        elif not isinstance(purchases_date, dtime.date):
            logging.error("purchases_date must be a date object or a string in YYYY-MM-DD format.")
            return False
        
        if purchases_date > dtime.datetime.now().date():
            logging.error("Purchase date cannot be in the future.")
            return False

        try:
            customers_id=int(customers_id)
            item_id=int(item_id)
            store_id=int(store_id)
            quantity=int(quantity)
        except ValueError:
            logging.error("customers_id, item_id, store_id, and quantity must be integers.")
            return False

        cursor=conn.cursor()
        # Check if customers_id, item_id, and store_id exist
        cursor.execute("SELECT 1 FROM  customers WHERE customer_id=%s",(customers_id,))
        if cursor.fetchone() is None:
            logging.error("customers douse not exist")
            return False
        # Check if item_id exists
        cursor.execute("SELECT 1 FROM items WHERE item_id=%s",(item_id,))
        if cursor.fetchone() is None:
            logging.error("item does not exist")
            return False
        # Check if store_id exists
        cursor.execute("SELECT 1 FROM stores WHERE store_id=%s",(store_id,))
        if cursor.fetchone() is None:
            logging.error("store does not exist")
            return False
        
            #check statuses
        try:
            cursor.execute("SELECT status FROM stores WHERE store_id=%s",(store_id,))
            store_status = cursor.fetchone()
            if store_status[0] != 'open':
                logging.warning("store %s is not open",store_id)
                return False
            cursor.execute("SELECT status FROM items WHERE item_id=%s",(item_id,))
            item_status = cursor.fetchone()
            if item_status[0] != 'active':
                logging.warning("item %s is not active",item_id)
                return False
            cursor.execute("SELECT status FROM inventory WHERE store_id=%s AND item_id=%s",(store_id,item_id))
            inventory_status = cursor.fetchone()
            if inventory_status is None or inventory_status[0] !='active':
                logging.warning("item %s is not active in store %s",item_id,store_id)
                return False
        except psycopg2.Error as e:
            logging.exception(f"data error in purchases.py: {e} ")
            return False
        
        # Check if item is in inventory
        cursor.execute("SELECT quantity FROM inventory WHERE store_id=%s AND item_id=%s",(store_id,item_id))
        number=cursor.fetchone()
        if not number:
            logging.error("item not in inventory")
            return None
        
        number=int(number[0])
        inventory_quantity=number-quantity

        if inventory_quantity<0:
            logging.error("to few items in the inventory")
            return False

        if inventory_quantity==0:
            status='inactive'

        cursor.execute("""INSERT INTO purchases 
                       (customers_id, item_id, store_id, quantity,purchases_date)
                   VALUES (%s,%s,%s,%s,%s) """,(customers_id,item_id,store_id,quantity,purchases_date))
        
        # update inventory table
        cursor.execute("""UPDATE inventory
                           SET quantity=%s,status=%s
                           WHERE store_id = %s AND item_id = %s""",(inventory_quantity,status,store_id,item_id))
            
        conn.commit()
        return inventory_quantity

    except psycopg2.Error as e:
        logging.exception(f"data error purchases.py: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()




    