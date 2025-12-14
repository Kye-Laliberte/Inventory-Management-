import psycopg2
import random
def additems(conn,name,category,price,tags,status='active'):
    """Adds an item to the items table """
    try:
        cursor=conn.cursor()
        if name is None or price is None:
            print("name and price are required.")
            return False
        
        if status not in ['active','inactive']:
            print("not a valid status")
            return False
        
        if price<0:
            print("price cannot be negative")
            return False
        
        # Check if item with same name and category exists
        cursor.execute("SELECT category_id FROM categorys WHERE name=%s;", (category,))
        category_id = cursor.fetchone()
        if category_id is None:
            print("category does not exist")
            return None
        category_id =int(category_id[0])

        # Check if item with same name and category exists
        cursor.execute("SELECT 1 FROM items WHERE name=%s AND category_id=%s",(name,category_id))
        row=cursor.fetchone()
        if row is not None:
            print("item alredy exits")
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
        print("item already exists.")
        return None
    except psycopg2.Error as e:
        print(f"data error {e}")
        return False
    finally:
        cursor.close()
