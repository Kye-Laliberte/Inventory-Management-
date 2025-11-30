import sqlite3
import os
db_path = 'app.db'
def setup(schema_path="Store.sql"):
    """Creates tables from SQL file"""
    if not os.path.exists(schema_path):
        raise FileExistsError(f"file not found: {schema_path}")
    
    conn=sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        with open(schema_path, "r", encoding="utf-8") as file:
            schema_sql =file.read()
        cursor.executescript(schema_sql)
        print("Tables created successfully.")
        
        customers=[
            ("Bill Gray","216-211-1231","myemail@gmail.com",0,'active'),
            ("Mark Dare","253-262-1331","just-a-guy@gmail.com",1,'active'),
            ('Alice Johnson', '555-1234', "alice@gmail.com", 1, 'active'),
            ('Bob Smith', "555-5678", "bob@icoud.com", 2, 'active'),
            ('Charlie Lee', "555-8765", "charlie@gmail.com", 0, 'inactive')
        ]
        cursor.executemany("""INSERT OR IGNORE INTO customers (name, phone, email, customers_tear, status)
                           VALUES(?,?,?,?,?);""",customers)
        
        stores=[
            ('Main st Store',"123 Main St",'closed'),
            ('High St Store',"456 High St",'open'),
            ('Oak St Store',"789 Oak St",'open'),
        ]

        cursor.executemany("""INSERT OR IGNORE INTO stores (name, location, status )
                           VALUES(?,?,?);""",stores)
        items=[
            ("eggs","food",12.51,'active',"food and baking product"),
            ("6 roll toilet paper","cleaning",20.25,'active',"cleaning and bathroom."),
            ('Laptop', 'electronics', 999.99, 'active', 'computers,tech'),
            ('Headphones', 'electronics', 199.99, 'active', 'audio,gadgets'),
            ('Coffee Mug', 'home', 12.5, 'active', 'kitchen,drinkware')
            ]
        cursor.executemany("""INSERT OR IGNORE INTO items(name, category, price, status, tags)
                           VALUES(?,?,?,?,?);""",items)
        
        
        inv = [
            (1, 3, 10),
            (1, 4, 15),
            (2, 4, 5),
            (2, 2, 30),
            (3, 5, 20),
            (1, 2, 4)]
        cursor.executemany("""INSERT INTO inventory (store_id, item_id, quantity) VALUES(?,?,?);""",inv)
        print("INSERT INTO inventory")

        conn.commit()
        print("Seed data inserted")
    except sqlite3.Error as e:
        print(f"data errer {e}")
    finally:
         conn.close()

if __name__ == "__main__":
    setup()