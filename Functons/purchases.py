import sqlite3
import datetime 
def addpurchase(customers_id, item_id,store_id,quantity,purchases_date,db_path="app.db"):
    """adds a purchase reaturns True if added False if error and none if sumthing is missing"""
    if quantity<=0:
        print("must be at least one item")
        return False
    

    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    try:

        cursor.execute("SELECT 1 FROM  customers WHERE customers_id=?",(customers_id,))
        if cursor.fetchone() is None:
            print("customers douse not exist")
            return False

        cursor.execute("SELECT 1 FROM items WHERE item_id=?",(item_id,))
        if cursor.fetchone() is None:
            print("item does not exist")
            return False

        cursor.execute("SELECT 1 FROM stores WHERE store_id=?",(store_id,))
        if cursor.fetchone() is None:
            print("store does not exist")
            return False
        

        cursor.execute("SELECT quantity FROM inventory WHERE store_id=? AND item_id=?",(store_id,item_id))
        number=cursor.fetchone()
        if not number:
            print("item not in inventory")
            return False
        
        if number[0]<=quantity:
            print("not enuff item in the inventory")
            return False
        
        cursor.execute("""INSERT INTO purchases 
                       (customers_id, item_id, store_id, quantity,purchases_date)
                   VALUES (?,?,?,?,?) """,(customers_id,item_id,store_id,quantity,purchases_date))
        
        cursor.execute("""
        UPDATE inventory
        SET quantity = quantity - ?
        WHERE item_id=? AND store_id=?""",
        (quantity, item_id, store_id))

        print(quantity)
        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"data ererror {e}")
        return False
    finally:
        conn.close()


if __name__=="__main__":
    addpurchase(1,2,1,2,"2025/05/25")



    