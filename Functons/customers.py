
import psycopg2
import logging
from psycopg2.extras import RealDictCursor
Customers_stat=['active','inactive']
def addCustomers(conn,name,phone,email,customer_tier=0,status='active'):
    """adds a Customers within the sql table constrants
    conn: psycopg2 connection object to the database.
    name: str - The name of the customer.
    phone: str - The phone number of the customer.
    email: str - The email address of the customer.
    customer_tier: int - The tier level of the customer (default is 0).
    status: str - The status of the customer (default is 'active').
    Returns:
        int: The new customer's ID if added successfully.
        False: If an error occurs or input is invalid.
        None: If the email or phone number is already taken.
    """
    cursor=None
    try:
        if not name or not phone or not email:
            logging.error("name, phone, and email are required.")
            return False
        try:
            customer_tier=int(customer_tier)
            name=str(name).strip()
            phone=str(phone).strip()
            email=str(email).strip()
            status=str(status).strip().lower()
        except ValueError:
            logging.error("incorect inputs.")
            return False

        if status not in Customers_stat:
            logging.error("not a valid status")
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
            logging.info("Email is already taken.")
        elif "phone" in str(l):
            logging.info("Phone is already taken.")
        else:
            logging.info("Integrity error occurred.")
        return None
    
    except psycopg2.Error as e:
        logging.exception(f"data error customers.py: {e}")
        return False

    finally:
            if cursor is not None:
                cursor.close()

def getCustumerByID(conn, customer_id):
    """Retrieves a customer's details by their ID.
    conn: psycopg2 connection object to the database.
    customer_id: int - The ID of the customer.
    Returns:
        dict: A dictionary containing the customer's details if found.
        None: If the customer is not found or an error occurs.
    """
    cursor=None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            logging.info("Customer not found.")
            return None
    except psycopg2.Error as e:
        logging.exception(f"data error customers.py: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()