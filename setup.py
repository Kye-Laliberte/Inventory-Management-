from genericpath import exists
import os
import random
import psycopg2
import logging

def setup(schema_path="Store.sql"):
    """Creates tables from SQL file"""

    if not exists(schema_path):
        raise FileNotFoundError(f"file not found: {schema_path}")
    
    conn=psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost",port="5432")
    cursor = conn.cursor()

    try:
        with open(schema_path, "r", encoding="utf-8") as file:
            sql = file.read()
     
        cursor.execute(sql)

        logging.info("Tables created successfully.")

        # Seed data for customers
        first_names = ["Bill", "Mark", "Alice", "Bob", "Charlie","Sally", "Diana", "Clark", "Bruce", "Lois", "Barry", "Kye"]
        last_names = ["Gray", "Dare", "Johnson", "Smith", "Lee","Chopper", "Prince", "Kent", "Wayne", "Lane", "Allen", "Laliberte"]
        email_domains = ["gmail.com", "yahoo.com", "outlook.com", "icloud.com"]
        statuses = ["active", "inactive"]
        
        emails_set = set()
        customers = []
        while len(customers) < 15:
            first = random.choice(first_names)
            last = random.choice(last_names)
            name = f"{first} {last}"
            phone = f"555-01{random.randint(10,99)}"
            email = f"{first.lower()}.{last.lower()}{random.randint(1,100)}@{random.choice(email_domains)}"

            if email in emails_set:
                continue
            emails_set.add(email)

            tier = random.randint(0,5)
            status = random.choice(statuses)
            customers.append((name, phone, email, tier, status))
        
        cursor.executemany("""INSERT  INTO customers (name, phone, email, customers_tier, status)
                           VALUES(%s,%s,%s,%s,%s)
                           ON CONFLICT (email)  DO NOTHING;""",customers)
        logging.info("INSERT INTO customers")

        # Seed data for stores
        store_names = ["Main", "High", "Oak", "Pine", "Maple", "Elm", "Cedar", "Lakeview", "Hilltop", "Sunset"]
        street_types = ["St", "Ave", "Blvd", "Rd", "Lane", "Drive"]
        store_statuses = ["open", "closed", "maintenance"]
        
        stores_set = set()
        stores = []

        while len(stores) < 7:
            name = f"{random.choice(store_names)} Store"
            
            location = f"{random.randint(100,999)} {random.choice(store_names)} {random.choice(street_types)}, Cityville, ST {random.randint(10000,99999)}"
            status = random.choice(store_statuses)
            # Generate unique store_code
            startcode=f"{name[:3].upper()}"
            storecode=f"{startcode}-{random.randint(100,999)}"
            
            if storecode in stores_set:
                continue
            stores_set.add(storecode)

        stores.append((name, location, status, storecode))

        cursor.executemany("""INSERT INTO stores (name, location, status, store_code)
                           VALUES(%s,%s,%s,%s)
                           ON CONFLICT (store_code) DO NOTHING;""",stores)
        logging.info("INSERT INTO stores")

        items_categories = ("home", "toys", "cleaning", "electronics", "food", "clothes")
        price_ranges = {"food": (1, 50),"cleaning": (5, 50),"electronics": (50, 2000),"home": (5, 500),"clothes": (10, 300),"toys": (5, 200)}
        sample_items = {
        "food": ["Eggs", "Milk", "Bread", "Cheese", "Apples"],
        "cleaning": ["Toilet Paper", "Detergent", "Broom", "Sponge", "Dish Soap"],
        "electronics": ["Laptop", "Headphones", "Smartphone", "Camera", "Monitor"],
        "home": ["Coffee Mug", "Cushion", "Lamp", "Plate Set", "Blanket"],
        "clothes": ["T-Shirt", "Jeans", "Jacket", "Socks", "Hat"],
        "toys": ["Action Figure", "Doll", "Puzzle", "Board Game", "RC Car"]}
        items = []
        item_codes_set = set()

        # Seed data for items
        for category in items_categories:
            for item_name in sample_items[category]:
                price_min, price_max = price_ranges[category]
                price = round(random.uniform(price_min, price_max), 2)
                status = random.choice(statuses)
                tags = f"{category},{item_name.lower()}"
                
                # Generate unique item_code
                base_code = f"{category[:3].upper()}{item_name[:3].upper()}"
                suffix = 1
                item_code = f"{base_code}-{suffix:03d}"
                while item_code in item_codes_set:
                    suffix += 1
                    item_code = f"{base_code}-{suffix:03d}"
                item_codes_set.add(item_code)

                items.append((item_code, item_name, category, price, status, tags))
         
        cursor.executemany("""INSERT INTO items(item_code, name, category, price, status, tags)
                           VALUES(%s,%s,%s,%s,%s,%s) ON CONFLICT (item_code) DO NOTHING;""",items)
        logging.info("INSERT INTO items")

        # Seed data for inventory
        inv = []
        assigned_inv = set()
        
        cursor.execute("SELECT store_id FROM stores;")
        store_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT item_id FROM items;")
        item_ids = [row[0] for row in cursor.fetchall()]

        for store_id in store_ids:
            sampled_items = random.sample(item_ids, k=min(10, len(item_ids)))
            for item_id in sampled_items:
                if (store_id, item_id) in assigned_inv:
                    continue
                assigned_inv.add((store_id, item_id))
                quantity = random.randint(0, 100)
                status = "inactive" if  quantity == 0 else "active"

                inv.append((store_id, item_id, quantity, status))

        cursor.executemany("""INSERT INTO inventory (store_id, item_id, quantity, status) VALUES(%s,%s,%s,%s) 
                           ON CONFLICT (store_id, item_id) DO NOTHING;""",inv)
        logging.info("INSERT INTO inventory")

        conn.commit()
        logging.info("Seed data inserted")


    except psycopg2.Error as e:
        logging.exception(f"data error setup.py: {e}")
    finally:
         conn.close()

if __name__ == "__main__":
    setup()