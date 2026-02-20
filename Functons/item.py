import psycopg2
import random
from psycopg2.extras import RealDictCursor
import logging


def additems(conn,name,category,price,tags,status='active',description=None):
    """Adds an item to the items table
    conn: psycopg2 connection object to the database.
    name: str - The name of the item.
    category: str - The category of the item.
    price: float - The price of the item.
    tags: str - Comma-separated tags for the item.
    status: str - The status of the item (default is 'active').
    description: str - The description of the item (default is None).
    """
    if description is not None:
        description=str(description).strip()

    cursor=None
    try:
        cursor=conn.cursor()
        if name is None or price is None or category is None:
            logging.error("name, price, and category are required.")
            return False
        
        name=str(name).strip()
        price=float(price)
        status=str(status).strip().lower()
        category=str(category).strip().lower() if category else None
        tags=str(tags).strip() if tags else None
        if status not in ['active','inactive']:
            logging.error("not a valid status")
            return False
        
        if price<0:
            logging.error("price cannot be negative")
            return False
        
        # Check if item with same name and category exists
        cursor.execute("SELECT category_id FROM categorys WHERE name=%s;", (category,))
        category_id = cursor.fetchone()
        if category_id is None:
            logging.info("category does not exist")
            return False
        
        category_id =int(category_id[0])

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
    finally:
        if cursor is not None:
            cursor.close()

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
            conn.commit()
        return True
    
    except psycopg2.Error as e:
        logging.exception(f"data error in item.py updateItemStatus: {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("item_id must be an integer and status must be a string")
        return False

def getItemByID(conn,item_id):
    """Fetches an item from the items table by its ID.
    conn: psycopg2 connection object to the database.
    item_id: int - The ID of the item.
    Returns: dict: A dictionary containing the item's details
    if not found None or False if an error occurs."""
    cursor=None
    try:
        cursor=conn.cursor(cursor_factory=RealDictCursor)
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
    finally:
        if cursor is not None:
            cursor.close()

def get_ItemBy_item_code(conn,item_code):
    """Fetches an item from the items table by its item_code.
    Item_code: str - The unique code.
    Returns: dict: A dictionary containing the item's details if found, None if not found, 
    or False if an error occurs."""
    curser=None
    try:
        item_code=str(item_code).strip()
        
        if not item_code:
            logging.error("item_code is cannot be empty")
            return False
        elif not isinstance(item_code, str):
            logging.error("item_code must be a string")
            return False
        elif len(item_code) != 10:
            logging.error("item_code must be exactly 10 characters long")
            return False
        
        curser=conn.cursor(cursor_factory=RealDictCursor)

        curser.execute("""SELECT * FROM items WHERE item_code = %s;""",(item_code,))
        
        item=curser.fetchone()

        if not item:
            logging.info("No item found with item_code=%s", item_code)
            return None
        
        return item
    
    except psycopg2.Error as e:
        logging.exception(f"Data error in item.py get_item_by_item_code: {e}")
        return False
    finally:
        if curser is not None:
            curser.close()