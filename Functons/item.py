import psycopg2
import random
import logging

def additems(conn,name,category,price,tags,status='active'):
    """Adds an item to the items table """
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
        cursor.execute("""INSERT INTO items (name,item_code,category_id,price,status,tags) 
                       VALUES (%s,%s,%s,%s,%s,%s) RETURNING item_id, item_code""",(name,itemcode,category_id,price,status,tags))
        conn.commit()
        return cursor.fetchone()[0]# Return the new item's ID and item_code

    except psycopg2.IntegrityError:
        logging.info("item already exists.")
        return None
    except psycopg2.Error as e:
        logging.exception(f"data error {e}")
        return False
    finally:
        cursor.close()
