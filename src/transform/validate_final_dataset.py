import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

orders = pd.read_csv(DATA_DIR / "orders_final.csv")
customers = pd.read_csv(DATA_DIR / "customers_clean.csv")
products = pd.read_csv(DATA_DIR / "products_clean.csv")


def check(condition, message):
    if condition:
        print(f"PASS: {message}")
    else:
        raise ValueError(f"FAILED: {message}")


print("\nFINAL DATA QUALITY CHECKS")
print("=" * 45)

check(
    orders["order_id"].is_unique,
    "Order IDs are unique"
)

check(
    orders["customer_id"].isin(customers["customer_id"]).all(),
    "All customer references are valid"
)

check(
    orders["product_id"].isin(products["product_id"]).all(),
    "All product references are valid"
)

check(
    (orders["quantity"] > 0).all(),
    "Quantity is positive"
)

check(
    (orders["unit_price"] > 0).all(),
    "Unit price is positive"
)

check(
    orders["discount"].between(0, 1).all(),
    "Discount is within valid range"
)

check(
    orders["order_date"].notna().all(),
    "Order dates are valid"
)

check(
    orders["order_total"].notna().all(),
    "Order totals are not missing"
)

print("=" * 45)
print("ALL FINAL QUALITY CHECKS PASSED!")
print("Rows ready for warehouse:", len(orders))