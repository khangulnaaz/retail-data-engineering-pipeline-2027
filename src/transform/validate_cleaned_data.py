"""
Retail Data Engineering Pipeline
Cleaned Data Quality Gates

Purpose:
Validate cleaned datasets before loading into MySQL.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "processed"


def check(condition: bool, message: str) -> None:
    """Raise an error when a validation rule fails."""

    if not condition:
        raise ValueError(f"QUALITY CHECK FAILED: {message}")

    print(f"PASS: {message}")


def main():

    orders = pd.read_csv(DATA_DIR / "orders_clean.csv")

    customers = pd.read_csv(DATA_DIR / "customers_clean.csv")

    products = pd.read_csv(DATA_DIR / "products_clean.csv")

    print("\n" + "=" * 55)
    print("CLEANED DATA VALIDATION")
    print("=" * 55)

    # 1. Primary key uniqueness
    check(
        orders["order_id"].is_unique,
        "Order IDs are unique"
    )

    check(
        customers["customer_id"].is_unique,
        "Customer IDs are unique"
    )

    check(
        products["product_id"].is_unique,
        "Product IDs are unique"
    )

    # 2. Required IDs
    check(
        orders["order_id"].notna().all(),
        "Order IDs are not missing"
    )

    check(
        customers["customer_id"].notna().all(),
        "Customer IDs are not missing"
    )

    check(
        products["product_id"].notna().all(),
        "Product IDs are not missing"
    )

    # 3. Referential integrity
    valid_customer_ids = set(customers["customer_id"])

    valid_product_ids = set(products["product_id"])

    check(
        orders["customer_id"].isin(valid_customer_ids).all(),
        "All order customer IDs exist"
    )

    check(
        orders["product_id"].isin(valid_product_ids).all(),
        "All order product IDs exist"
    )

    # 4. Quantity validation
    check(
        (orders["quantity"].dropna() > 0).all(),
        "Order quantities are positive"
    )

    # 5. Price validation
    check(
        (orders["unit_price"].dropna() > 0).all(),
        "Order prices are positive"
    )

    check(
        (products["unit_price"].dropna() > 0).all(),
        "Product prices are positive"
    )

    # 6. Discount validation
    check(
        orders["discount"].dropna().between(0, 1).all(),
        "Discounts are between 0 and 1"
    )

    # 7. Date validation
    check(
        orders["order_date"].notna().all(),
        "Order dates are valid"
    )

    # 8. Order total validation
    expected_total = (
        orders["quantity"]
        * orders["unit_price"]
        * (1 - orders["discount"])
    ).round(2)

    actual_total = orders["order_total"].round(2)

    total_matches = (
        expected_total.isna() & actual_total.isna()
    ) | (
        expected_total.notna()
        & actual_total.notna()
        & expected_total.eq(actual_total)
    )

    check(
        total_matches.all(),
        "Order totals match calculated values"
    )

    print("\n" + "=" * 55)
    print("ALL QUALITY GATES PASSED!")
    print("=" * 55)

    print("\nDataset summary:")

    print(f"Customers: {len(customers)}")

    print(f"Products: {len(products)}")

    print(f"Orders: {len(orders)}")


if __name__ == "__main__":
    main()