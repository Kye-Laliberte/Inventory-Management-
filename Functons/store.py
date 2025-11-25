import sqlite3
storestatas=['open','closed','maintenance']
def addstore(name,location,status='open',db_path='app.db'):
    """adds a store to the store table"""
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    try:

        if  status not in storestatas:
            print(f"{status} is not a valid status")
            return False
        
        cursor.execute("SELECT 1 FROM stores WHERE name=?", (name,))
        if cursor.fetchone() is not None:
            print("store already exists")
            return None
        
        cursor.execute("INSERT INTO stores (name,location,status) VALUES (?,?,?)",(name,location,status))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"data ererro{e}")
        return False
    finally:
        conn.close()
    