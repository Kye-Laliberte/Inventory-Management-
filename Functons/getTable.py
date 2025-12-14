import psycopg2
import logging
def getTable(conn, table_name):
    """Fetches all records from the specified table."""
    try:
        if table_name is None or not isinstance(table_name, str):
            logging.error("A valid table name is required.")
            return []
        table_name = table_name.strip().lower()
        if table_name not in ['customers', 'items', 'stores', 'purchases', 'categorys','inventory']:
            logging.error("Invalid table name.")
            return []

        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except psycopg2.Error as e:
        logging.exception(f"Error fetching data from {table_name}: {e}")
        return []
    finally:
        cursor.close()