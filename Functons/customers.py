
import sqlite3
Customers_stat=['active','inactive']
def addCustomers(name,phone,email,customers_tear=0,status='active',db_path='app.db'):
    """"adds a Customers within the sql table constrants"""
    conn =sqlite3.connect(db_path)
    cursor=conn.cursor()
    try:
        
        
        if status not in Customers_stat:
            print("not a valid status")
            return False
        
        if customers_tear<0 or customers_tear>3:
            return False
        
        cursor.execute("""SELECT name 1 customers WHERE phone=? OR email=?""",(phone,email))
        if cursor.fetchone() is not None:
            print("phone or email is already taken.")
            return None
        
        cursor.execute("""INSERT INTO customers (name,phone,email,customers_tear,status)
                       VALUES (?,?,?,?,?)""",(name,phone,email,customers_tear,status))
        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"data error {e}")
        return False
    finally:
        conn.close()

