CREATE TABLE IF NOT EXISTS customers(
   customers_id INTEGER Primary KEY   AUTOINCREMENT,
    name TEXT NOT NULL
    phone TEXT UNIQUE,
    email TEXT UNIQUE,
    customers_tear INTEGER NOT NULL DEFAULT 0 CHECK(customers_tear>=0 and customers_tear<=3),
    STATUS, NOT NULL DEFAULT 'active'  CHECK(STATUS IN('active','inactive'))
);



CREATE TABLE IF NOT EXISTS stores(
   store_id INTEGER Primary KEY   AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT, 
    status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'closed', 'renovation'))
);

CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive')),
    tags TEXT
);

CREATE TABLE IF NOT EXISTS inveintory(
   store_id INTEGER,
   item_id INTEGER,
   quantity INTEGER NOT NULL CHECK(quantity>0),
   Primary KEY (store_id,item_id),
   FOREIGN KEY (store_id)REFERENCES stores(store_id),
   FOREIGN KEY (item_id)REFERENCES items(item_id)

);
CREATE TABLE IF NOT EXISTS purchases(
    purchases_id INTEGER PRIMARY KEY   AUTOINCREMENT,
    customers_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    quantity INTEGER CHECK(quantity>0),
    purchases_date DATETIME not NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customers_id) REFERENCES customers(customers_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (store_id)REFERENCES stores(store_id)
);

