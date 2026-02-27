
CREATE TABLE IF NOT EXISTS customers(
   customer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE NOT NULL,
    customers_tier INTEGER NOT NULL DEFAULT 0 CHECK (customers_tier BETWEEN 0 AND 5),
    status TEXT NOT NULL DEFAULT 'active'  CHECK (status IN('active','inactive'))
);

CREATE TABLE IF NOT EXISTS stores(
   store_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,  
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('inactive', 'active')),
    store_code TEXT UNIQUE NOT NULL, --first three letters of store name + three digit number 
    ADD CONSTRAINT name_location UNIQUE (name, location)
);

CREATE TABLE  IF NOT EXISTS categorys(
    category_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,--home toys cleaning electronics food clothes 
    description TEXT
);

CREATE TABLE IF NOT EXISTS  items (
    item_id SERIAL PRIMARY KEY,
    item_code VARCHAR(10) NOT NULL UNIQUE, --first three letters of category + first three letters of item name + - + three digit number 
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categorys(category_id),
    description TEXT,
    price NUMERIC(10,2) NOT NULL CHECK(price >= 0),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive')),
    tags TEXT
);

CREATE TABLE IF NOT EXISTS inventory(
   store_id INTEGER REFERENCES stores(store_id),
   item_id INTEGER REFERENCES items(item_id), 
   Primary KEY (store_id,item_id),
   quantity INTEGER NOT NULL CHECK(quantity>=0) DEFAULT 0,
   status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive'))
  
);
CREATE TABLE IF NOT EXISTS purchases(
    purchases_id SERIAL PRIMARY KEY,
    customers_id INTEGER NOT NULL REFERENCES customers(customer_id),
    item_id INTEGER NOT NULL REFERENCES items(item_id),
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    quantity INTEGER CHECK(quantity>0),
    purchases_date TIMESTAMP NOT NULL DEFAULT NOW()

);

