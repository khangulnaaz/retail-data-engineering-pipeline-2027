"""
Retail Data Engineering Pipeline
Raw Data Validation

Checks business rules, duplicates and referential integrity.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

REPORT_DIR = PROJECT_ROOT / "data" / "processed"


def main():

    orders = pd.read_csv(RAW_DATA_DIR / "orders_raw.csv")

    customers = pd.read_csv(RAW_DATA_DIR / "customers.csv")

    products = pd.read_csv(RAW_DATA_DIR / "products.csv")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    issues = []

    # 1. Duplicate order IDs
    duplicate_orders = orders[
        orders["order_id"].duplicated(keep=False)
    ]

    issues.append(
        duplicate_orders.assign(
            issue_type="duplicate_order_id"
        )
    )

    # 2. Missing customer IDs
    missing_customer = orders[
        orders["customer_id"].isna()
    ]

    issues.append(
        missing_customer.assign(
            issue_type="missing_customer_id"
        )
    )

    # 3. Invalid quantities
    invalid_quantity = orders[
        orders["quantity"].isna()
        | (orders["quantity"] <= 0)
    ]

    issues.append(
        invalid_quantity.assign(
            issue_type="invalid_quantity"
        )
    )

    # 4. Invalid unit prices
    invalid_price = orders[
        orders["unit_price"].isna()
        | (orders["unit_price"] <= 0)
    ]

    issues.append(
        invalid_price.assign(
            issue_type="invalid_order_price"
        )
    )

    # 5. Invalid discounts
    invalid_discount = orders[
        orders["discount"].isna()
        | (orders["discount"] < 0)
        | (orders["discount"] > 1)
    ]

    issues.append(
        invalid_discount.assign(
            issue_type="invalid_discount"
        )
    )

    # 6. Invalid order dates
    parsed_dates = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    invalid_dates = orders[
        parsed_dates.isna()
    ]

    issues.append(
        invalid_dates.assign(
            issue_type="invalid_order_date"
        )
    )

    # 7. Orphan customer references
    orphan_customers = orders[
        orders["customer_id"].notna()
        & ~orders["customer_id"].isin(customers["customer_id"])
    ]

    issues.append(
        orphan_customers.assign(
            issue_type="customer_not_found"
        )
    )

    # 8. Orphan product references
    orphan_products = orders[
        orders["product_id"].notna()
        & ~orders["product_id"].isin(products["product_id"])
    ]

    issues.append(
        orphan_products.assign(
            issue_type="product_not_found"
        )
    )

    # 9. Duplicate customer IDs
    duplicate_customers = customers[
        customers["customer_id"].duplicated(keep=False)
    ]

    print("\nDuplicate Customer IDs:")
    print(duplicate_customers)

    # 10. Duplicate product IDs
    duplicate_products = products[
        products["product_id"].duplicated(keep=False)
    ]

    print("\nDuplicate Product IDs:")
    print(duplicate_products)

    # Combine order-level validation issues
    order_issues = pd.concat(
        issues,
        ignore_index=True
    )

    # Summary
    print("\n" + "=" * 60)
    print("DATA VALIDATION SUMMARY")
    print("=" * 60)

    print(
        order_issues["issue_type"]
        .value_counts()
        .to_string()
    )

    # Save detailed issues
    output_path = REPORT_DIR / "validation_issues.csv"

    order_issues.to_csv(
        output_path,
        index=False
    )

    print(f"\nValidation issues saved to: {output_path}")

    print(
        f"\nTotal issue records: {len(order_issues)}"
    )


if __name__ == "__main__":
    main()