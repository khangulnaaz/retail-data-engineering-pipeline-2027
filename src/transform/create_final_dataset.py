
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Load datasets
orders = pd.read_csv(DATA_DIR / "orders_clean.csv")
customers = pd.read_csv(DATA_DIR / "customers_clean.csv")
products = pd.read_csv(DATA_DIR / "products_clean.csv")

# Valid customer and product IDs
valid_customer_ids = set(customers["customer_id"])
valid_product_ids = set(products["product_id"])

# Keep only valid orders

valid_orders = orders[
    orders["customer_id"].isin(valid_customer_ids)
    & orders["product_id"].isin(valid_product_ids)
    & orders["quantity"].notna()
    & (orders["quantity"] > 0)
    & orders["unit_price"].notna()
    & (orders["unit_price"] > 0)
    & orders["discount"].notna()
    & orders["discount"].between(0, 1)
    & pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    ).notna()
].copy()


# Save final dataset
valid_orders.to_csv(
    DATA_DIR / "orders_final.csv",
    index=False
)

print("=" * 45)
print("FINAL DATASET REPORT")
print("=" * 45)

print("Original orders:", len(orders))
print("Valid orders:", len(valid_orders))
print("Rejected orders:", len(orders) - len(valid_orders))

print("Final dataset saved successfully!")
