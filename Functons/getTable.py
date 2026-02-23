import psycopg2
import logging
def getTable(conn, table_name):
    """Fetches all records from the specified table.
    conn: psycopg2 connection object to the database.
    table_name: str - The name of the table to fetch records from.
     Returns:
        list: A list of tuples containing the records from the specified table."""
    try:
        
        table_name = str(table_name).strip().lower()

        if table_name not in ['customers', 'items', 'stores', 'purchases', 'categorys','inventory']:
            logging.error("Invalid table name.")
            return False

        with conn.cursor() as cursor:
            query = f"SELECT * FROM {table_name};"
            cursor.execute(query)
            records = cursor.fetchall()
        
        return records
    
    except psycopg2.Error as e:
        logging.exception(f"Error fetching data from {table_name}: {e}")
        return False
    except (ValueError, TypeError):
        logging.exception("input must be a string")
        return False