
import psycopg2
Customers_stat=['active','inactive']
def addCustomers(conn,name,phone,email,customer_tier=0,status='active'):
    """adds a Customers within the sql table constrants"""
    try:
        if not name or not phone or not email:
            print("name, phone, and email are required.")
            return False
        
        name=str(name).strip()
        phone=str(phone).strip()
        email=str(email).strip()
        status=str(status).strip().lower()
        customer_tier=int(customer_tier)

        if status not in Customers_stat:
            print("not a valid status")
            return False
        
        if customer_tier is None:
            customer_tier=0

        if customer_tier<0 or customer_tier>5:
            return False
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO customers (name,phone,email,customers_tier,status)
                       VALUES (%s,%s,%s,%s,%s) RETURNING customer_id""",(name,phone,email,customer_tier,status))
        conn.commit()
        return cursor.fetchone()[0]

    except psycopg2.IntegrityError as l:
        if "email" in str(l):
            print("Email is already taken.")
        elif "phone" in str(l):
            print("Phone is already taken.")
        else:
            print("Integrity error occurred.")
        return None
    except psycopg2.Error as e:
        print(f"data error {e}")
        return False

    finally:
        cursor.close()

