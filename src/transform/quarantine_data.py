
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Load cleaned datasets
orders = pd.read_csv(DATA_DIR / "orders_clean.csv")
customers = pd.read_csv(DATA_DIR / "customers_clean.csv")
products = pd.read_csv(DATA_DIR / "products_clean.csv")

# 1. Missing customer references
orphan_customers = orders[
    orders["customer_id"].notna()
    & ~orders["customer_id"].isin(customers["customer_id"])
].copy()

# 2. Missing product references
orphan_products = orders[
    orders["product_id"].notna()
    & ~orders["product_id"].isin(products["product_id"])
].copy()

# 3. Invalid quantity
invalid_quantity = orders[
    orders["quantity"].isna()
    | (orders["quantity"] <= 0)
].copy()

# 4. Invalid unit price
invalid_price = orders[
    orders["unit_price"].isna()
    | (orders["unit_price"] <= 0)
].copy()

# 5. Invalid discount
invalid_discount = orders[
    orders["discount"].isna()
    | ~orders["discount"].between(0, 1)
].copy()

# 6. Invalid order dates
invalid_dates = orders[
    pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    ).isna()
].copy()

# Save rejected records
rejected_datasets = {
    "rejected_orders_missing_customer.csv": orphan_customers,
    "rejected_orders_missing_product.csv": orphan_products,
    "rejected_orders_invalid_quantity.csv": invalid_quantity,
    "rejected_orders_invalid_price.csv": invalid_price,
    "rejected_orders_invalid_discount.csv": invalid_discount,
    "rejected_orders_invalid_date.csv": invalid_dates
}

for filename, dataframe in rejected_datasets.items():
    dataframe.to_csv(DATA_DIR / filename, index=False)

# Summary
print("=" * 45)
print("QUARANTINE REPORT")
print("=" * 45)

print("Missing customer records:", len(orphan_customers))
print("Missing product records:", len(orphan_products))
print("Invalid quantity records:", len(invalid_quantity))
print("Invalid unit price records:", len(invalid_price))
print("Invalid discount records:", len(invalid_discount))
print("Invalid order date records:", len(invalid_dates))

print("\nAll quarantine files saved successfully!")
