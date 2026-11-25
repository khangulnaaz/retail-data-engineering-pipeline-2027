
import pandas as pd
import mysql.connector
import getpass
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# MySQL connection
password = getpass.getpass("Enter MySQL root password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="retail_data_warehouse"
)

cursor = connection.cursor()

# --------------------------------
# 1. Load Customers
# --------------------------------

customers = pd.read_csv(DATA_DIR / "customers_clean.csv")

customer_query = """
INSERT IGNORE INTO customers
(customer_id, customer_name, email, city, state, signup_date)
VALUES (%s, %s, %s, %s, %s, %s)
"""

customer_data = [
    tuple(None if pd.isna(value) else value for value in row)
    for row in customers.itertuples(index=False, name=None)
]

cursor.executemany(customer_query, customer_data)
connection.commit()

print(f"Successfully loaded {cursor.rowcount} customer records!")

# --------------------------------
# 2. Load Products
# --------------------------------

products = pd.read_csv(DATA_DIR / "products_clean.csv")

product_query = """
INSERT IGNORE INTO products
(product_id, product_name, category, unit_price, stock_quantity, supplier)
VALUES (%s, %s, %s, %s, %s, %s)
"""

product_data = [
    tuple(None if pd.isna(value) else value for value in row)
    for row in products.itertuples(index=False, name=None)
]

cursor.executemany(product_query, product_data)
connection.commit()

print(f"Successfully loaded {cursor.rowcount} product records!")

# --------------------------------
# 3. Load Orders
# --------------------------------

orders = pd.read_csv(DATA_DIR / "orders_final.csv")

order_query = """
INSERT IGNORE INTO orders
(order_id, customer_id, product_id, order_date, quantity,
 unit_price, discount, payment_method, order_status, order_total)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

order_data = [
    tuple(None if pd.isna(value) else value for value in row)
    for row in orders.itertuples(index=False, name=None)
]

cursor.executemany(order_query, order_data)
connection.commit()

print(f"Successfully loaded {cursor.rowcount} order records!")

# --------------------------------
# Close Connection
# --------------------------------

cursor.close()
connection.close()

print("All datasets loaded successfully into MySQL!")
