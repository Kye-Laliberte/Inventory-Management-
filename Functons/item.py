import sqlite3
def additems(name,category,price,tags,status='active',dp_path="app.db"):
    """Adds an item to the items table"""
    try:
        conn=sqlite3.connect(dp_path)
        cursor=conn.cursor()
        cursor.execute("SELECT 1 FROM items WHERE name=? AND category=?",(name,category))
        
        row=cursor.fetchone()
        if row is not None:
            print("item alredy exits")
            return None
        
        cursor.execute("""INSERT INTO items (name,category,price,status,tags) 
                       VALUES (?,?,?,?,?)""",(name,category,price,status,tags))
        conn.commit()
        return True
    
    except sqlite3.Error as e:
        print(f"data ereror {e}")
        return False
    finally:
        conn.close()

#if __name__ == "__main__":
#    val=additems("toy car","toys",3.0,"fun for the kids")
#    print(val)