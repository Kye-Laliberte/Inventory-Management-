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
        
        
        cursor.execute("INSERT INTO stores (name,location,status) VALUES (?,?,?)",(name,location,status))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("store already at exists")
        return None
    except sqlite3.Error as e:
        print(f"data ererro{e}")
        return False
    finally:
        conn.close()
if  __name__ == "__main__":
    val=addstore("kyes best buy", "245cr3543")
    print(val)