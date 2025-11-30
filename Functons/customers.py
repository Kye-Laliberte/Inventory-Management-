
import sqlite3
Customers_stat=['active','inactive']
def addCustomers(name,phone,email,customer_tier=0,status='active',db_path='app.db'):
    """adds a Customers within the sql table constrants"""
    
    try:
        
        
        if status not in Customers_stat:
            print("not a valid status")
            return False
        
        if customer_tier<0 or customer_tier>3:
            return False
        

        conn =sqlite3.connect(db_path)
        cursor=conn.cursor()

        
        cursor.execute("""INSERT INTO customers (name,phone,email,customers_tear,status)
                       VALUES (?,?,?,?,?)""",(name,phone,email,customer_tier,status))
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        print("Phone or email is already taken.")
        return None
    except sqlite3.Error as e:
        print(f"data error {e}")
        return False

    finally:
        conn.close()

if __name__ == "__main__":
    val=addCustomers("Jon Dow",38232322323,"tester@yaho.com",1,'active')
    print(val)