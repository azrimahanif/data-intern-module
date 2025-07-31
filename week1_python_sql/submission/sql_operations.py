import sqlite3
import pandas as pd

# Baca data bersih
df = pd.read_csv("cleaned_data.csv")

# Sambung ke SQLite (akan cipta database jika belum ada)
conn = sqlite3.connect("customer_data.db")
cursor = conn.cursor()

# Cipta table customers
cursor.execute("""
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
)
""")

# Masukkan data ke dalam table
df.to_sql("customers", conn, if_exists="replace", index=False)

# Query: Most popular product categories
popular_categories = cursor.execute("""
SELECT product_category, COUNT(*) as count
FROM customers
GROUP BY product_category
ORDER BY count DESC
LIMIT 3
""").fetchall()

# Query: Average spending per country
avg_spending = cursor.execute("""
SELECT country, ROUND(AVG(amount), 2) as avg_amount
FROM customers
GROUP BY country
ORDER BY avg_amount DESC
""").fetchall()

# Query: Highest spending customer
highest_spender = cursor.execute("""
SELECT customer_name, MAX(amount)
FROM customers
""").fetchone()

# Query: Number of active customers
active_count = cursor.execute("""
SELECT COUNT(*) FROM customers
WHERE status = 'Active'
""").fetchone()[0]

# Output results
print("\n📦 Most Popular Product Categories:")
for category, count in popular_categories:
    print(f"- {category}: {count} customers")

print("\n💰 Average Spending per Country:")
for country, avg in avg_spending:
    print(f"- {country}: {avg}")

print("\n🏆 Highest Spending Customer:")
print(f"- {highest_spender[0]}: {highest_spender[1]}")

print(f"\n✅ Number of Active Customers: {active_count}")

# Tutup sambungan database
conn.close()
