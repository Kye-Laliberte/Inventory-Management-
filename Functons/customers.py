
import psycopg2
import logging
from psycopg2.extras import RealDictCursor
Customers_stat=['active','inactive']
def addCustomer(conn,name,phone,email,customer_tier=0,status='active'):
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
    
    try:
          
        try:
            customer_tier=int(customer_tier)
            name=str(name).strip()
            phone=str(phone).strip()
            email=str(email).strip()
            status=str(status).strip().lower()
            email=str(email).strip().lower()
        except (ValueError, TypeError):
            logging.error("incorect or invalid input types.")
            return False

        if status not in Customers_stat:
            logging.error("not a valid status")
            return False
        
        if customer_tier is None:
            customer_tier=0

        if customer_tier<0 or customer_tier>5:
            return False
        with conn.cursor() as cursor:

            cursor.execute("""INSERT INTO customers (name,phone,email,customers_tier,status)
                       VALUES (%s,%s,%s,%s,%s) RETURNING customer_id""",(name,phone,email,customer_tier,status))
            conn.commit()
            if cursor.rowcount == 0:
                logging.error("Failed to add customer.")
            val=cursor.fetchone()[0]

        return val

    except psycopg2.IntegrityError as l:
        if "email" in str(l):
            logging.info("Email is already taken.")
            return False
        elif "phone" in str(l):
            logging.info("Phone is already taken.")
            return False
        else:
            logging.info("Integrity error occurred.")
        return None
    
    except psycopg2.Error as e:
        logging.exception(f"data error customers.py: {e}")
        return False


def getCustumerByID(conn, customer_id):
    """Retrieves a customer's details by their ID.
    conn: psycopg2 connection object to the database.
    customer_id: int - The ID of the customer.
    Returns:
        dict: A dictionary containing the customer's details if found.
        None: If the customer is not found or an error occurs.
    """
    
    try:
        customer_id=int(customer_id)
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                logging.info("Customer not found.")
                return None
            
    except psycopg2.Error as e:
        logging.exception(f"data error customers.py: {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("customer_id must be an integer")
        return False
    
def UpdateCustomerInfo(conn,customer_id,name=None,phone=None,email=None,customer_tier=None,status=None):
    """Updates a customer's information based on provided parameters.
    """
    try:
        customer_id=int(customer_id)
        status=str(status).strip().lower() if status is not None else None
        name=str(name).strip() if name is not None else None
        phone=str(phone).strip() if phone is not None else None
        email=str(email).strip().lower() if email is not None else None
        customer_tier=int(customer_tier) if customer_tier is not None else None
        if status not in Customers_stat:
            logging.error("not a valid status")
            return False
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            if cursor.fetchone() is None:
                logging.warning(f"Customer not found with ID {customer_id}")
                return False
            update_fields = []
            update_values = []
            if name is not None:
                update_fields.append("name =%s")
                update_values.append(name)

            if phone is not None:
                update_fields.append("phone =%s")
                update_values.append(phone)
            if email is not None:                    
                update_fields.append("email =%s")
                update_values.append(email)
            if customer_tier is not None:
                update_fields.append("customer_tier =%s")
                update_values.append(customer_tier)
            if status is not None:
                 update_fields.append("status =%s")
                 update_values.append(status)
                
            if update_fields:
                query = f"UPDATE customers SET {', '.join(update_fields)} WHERE customer_id = %s"
                update_values.append(customer_id)
                cursor.execute(query, tuple(update_values))
                conn.commit()
                logging.info(f"Customer with ID {customer_id} updated successfully.")
                return True
            else:
                logging.warning("No fields to update.")
                return True
    except psycopg2.Error as e:
        logging.exception(f"data error customers.py: {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("customer_id must be an integer")
        return False