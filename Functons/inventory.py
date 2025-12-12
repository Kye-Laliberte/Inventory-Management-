import sqlite3
def addToInventory(store_id,item_id,newquantity,db_path="app.db"):
    """Updatas the Inventory quantity or add a new Inventory"""
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()

    if newquantity<0:
        return False

    try:
        cursor.execute("SELECT 1 FROM stores WHERE store_id=?",(store_id,))
        if cursor.fetchone() is None:
            print("no store")
            return False
        cursor.execute("SELECT 1 FROM items WHERE item_id=?",(item_id,))
        if cursor.fetchone() is None:
            print("no item")
            return False

        cursor.execute("SELECT quantity FROM inventory WHERE store_id=? AND item_id=?",(store_id,item_id))
        row=cursor.fetchone()
        
        if (row):
            quantity=row[0]
            if(quantity==newquantity):
                print("quantity already matches")
                return None
            
            cursor.execute("""UPDATE inventory
                           SET quantity=?
                           WHERE store_id = ? AND item_id = ?""",(newquantity,store_id,item_id))
            conn.commit()
            return True

        else:  
            cursor.execute("""INSERT INTO inventory (store_id,item_id,quantity)  
                       VALUES (?,?,?)""",(store_id,item_id,newquantity))
            conn.commit()
            return True

    except sqlite3.Error as e:
        print(f"data error {e}")
        return False
    finally:
        conn.close()


if __name__=="__main__":
    v=addToInventory(1,3,17)
    print(v)