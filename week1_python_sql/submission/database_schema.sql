CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    age INTEGER,
    city TEXT,
    state TEXT,
    country TEXT,
    signup_date TEXT,
    last_purchase TEXT,
    product_category TEXT,
    amount REAL,
    currency TEXT,
    rating REAL,
    status TEXT
);
