import psycopg2
import random
from psycopg2.extras import RealDictCursor
import logging
from ..data.conect import get_connection

def additem(name,category_id,price,tags,status='active',description=None):
    
    if description is not None:
        description=str(description).strip()
    try:
            if name is None or price is None or category is None:
                logging.error("name, price, and category are required.")
                return False
    
            name=str(name).strip().lower()
            price=float(price)
            status=str(status).strip().lower()
            category=str(category).strip().lower() if category else None
            tags=str(tags).strip() if tags else None

            if status not in ['active','inactive']:
                logging.error("not a valid status")
                return False
                    
            if price<0:
                logging.error("price cannot be negative or zero")
                return False
            
            category_id =int(category_id)

            with  get_connection() as conn:

                with conn.cursor() as cursor:
                # Check if item with same name and category exists
                    cursor.execute("SELECT 1 FROM items WHERE name=%s AND category_id=%s",(name,category_id))
                    row=cursor.fetchone()
                    if row is not None:
                        logging.info("item already exists")
                        return None
       
            #generate unique item_code
                    startcode=f"{category[:3].upper()}{name[:3].upper()}"
                    itemcode=f"{startcode}-001"
                    while True:
                        cursor.execute("SELECT 1 FROM items WHERE item_code=%s;", (itemcode,))
                        if cursor.fetchone() is None:
                            break
                        itemcode=f"{startcode}-{random.randint(100,999)}"
                    cursor.execute("""INSERT INTO items (name,item_code,category_id,description,price,status,tags) 
                       VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING item_id, item_code""",(name,itemcode,category_id,description,price,status,tags))
                    conn.commit()
                    return cursor.fetchone()[0]# Return the new item's ID and item_code

    except psycopg2.IntegrityError:
        logging.info("item already exists.")
        return None
    except psycopg2.Error as e:
        logging.exception(f"data error item.py additems: {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("invalid input: price must be a float/Int and name, category, tags, description must be STRING")
    
def updateItemStatus(conn,item_id,status):
    """Updates the status of an item in the items table."""
    try:
        item_id=int(item_id)
        status=str(status).strip().lower()
        
        if status not in ['active','inactive']:
            logging.error("not a valid status")
            return False
        
        item_info=getItemByID(conn,item_id) # Check if item exists and is active
        if not item_info:
            logging.error("item not found will not update item status")
            return False
        
        elif item_info['status'] == status:
            logging.info("item already has the specified status")
            return True
        
        with conn.cursor() as cursor:
            cursor.execute("UPDATE items SET status=%s WHERE item_id=%s",(status,item_id))
            newitem=cursor.fetchone()
            conn.commit()
        return {"item_id": newitem[0],"item_code": newitem[1]}
    except psycopg2.Error as e:
        logging.exception(f"data error in item.py updateItemStatus: {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("item_id must be an integer and status must be a string")
        return False
    except psycopg2.IntegrityError as f:
        logging.info(f"IntegrityError: {f}.")
        return None

def updateItemInfo(conn,item_id,name=None,price=None,tags=None,description=None):
    """Updates the information of an item in the items table.
    can update name, price, tags, and description. item_id is required and other parameters are optional."""
    try:
        item_id=int(item_id)
        name=str(name).strip() if name else None
        price=float(price) if price is not None else None
        tags=str(tags).strip() if tags else None
        description=str(description).strip() if description else None
        update_field=[]
        update_values=[]

        if name is not None:
            update_field.append("name=%s")
            update_values.append(name)
        
        if price is not None:
            if price < 0:
                    logging.error("price must be a positive number")
                    return False
            update_field.append("price=%s")
            update_values.append(price)

        if tags is not None:
            update_field.append("tags=%s")
            update_values.append(tags)
            
        if description is not None:
            update_field.append("description=%s")
            update_values.append(description)
         
        if update_field:
            update_query = f"UPDATE items SET {', '.join(update_field)} WHERE item_id=%s"
            
            update_values.append(item_id)
            with conn.cursor() as cursor:
                cursor.execute(update_query, tuple(update_values))
                conn.commit()
            return True
        

    except (ValueError, TypeError):
        logging.exception("invalid input: item_id must be an integer, price must be a float/Int, and name, category, tags, description must be STRING")
        return False
    except psycopg2.Error as e:
        logging.exception(f"data error in item.py updateItemInfo: {e}")
        return False        


def getItemByID(conn,item_id):
    """Fetches an item from the items table by its ID.
    conn: psycopg2 connection object to the database.
    item_id: int - The ID of the item.
    Returns: dict: A dictionary containing the item's details
    if not found None or False if an error occurs."""
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            item_id=int(item_id)
            cursor.execute("SELECT * FROM items WHERE item_id=%s",(item_id,))
            
            item = cursor.fetchone()

        if item is None:
            logging.info("No item found with item_id=%s", item_id)
            return None
    
        return item
    
    except psycopg2.Error as e:
        logging.exception(f"data error in item.py get_item_by_id: {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("item_id must be an integer")
        return False
    
def get_ItemBy_item_code(conn,item_code):
    """Fetches an item from the items table by its item_code.
    Item_code: str - The unique code.
    Returns: dict: A dictionary containing the item's details if found, None if not found, 
    or False if an error occurs."""
    
    try:
        item_code=str(item_code).strip()
        
        if len(item_code) != 10:
            logging.error("item_code must be exactly 10 characters long")
            return False
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM items WHERE item_code = %s;""",(item_code,))
            
            item=cursor.fetchone()

        if not item:
            logging.info("No item found with item_code=%s", item_code)
            return None
        
        return item
    
    except psycopg2.Error as e:
        logging.exception(f"Data error in item.py get_item_by_item_code: {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("item_code must be a string")
        return False