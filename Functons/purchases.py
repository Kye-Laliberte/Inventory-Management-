import sqlite3
import datetime 
def addpurchase(customers_id, item_id,store_id,quantity,purchases_date,db_path="app.db"):
    """adds a purchase reaturns True if added False if error and none if sumthing is missing"""
    if quantity<=0:
        print("must be at least one item")
        return False
    
    try:
        datetime.datetime.strptime(purchases_date, "%Y-%m-%d")
    except ValueError:
        print("invalid date format, must be YYYY-MM-DD")
        return False

    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM  customers WHERE customers_id=?",(customers_id,))
        if cursor.fetchone() is None:
            print("customers douse not exist")
            return None

        cursor.execute("SELECT 1 FROM items WHERE item_id=?",(item_id,))
        if cursor.fetchone() is None:
            print("item does not exist")
            return None

        cursor.execute("SELECT 1 FROM stores WHERE store_id=?",(store_id,))
        if cursor.fetchone() is None:
            print("store does not exist")
            return None
    
        cursor.execute("SELECT 1 FROM purchases WHERE customers_id=? AND item_id=? AND store_id=? AND quantity=? AND purchases_date=?",(customers_id,item_id,store_id,quantity,purchases_date))

        if cursor.fetchone() is not None:
            print("repeat order")
            return None

        cursor.execute("""INSERT INTO purchases (customers_id, item_id, store_id, quantity,purchases_date)
                   VALUES (?,?,?,?,?) """,(customers_id,item_id,store_id,quantity,purchases_date))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"data ererror {e}")
        return False
    finally:
        conn.close()


    