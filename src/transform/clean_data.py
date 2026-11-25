"""
Retail Data Engineering Pipeline
Data Cleaning and Transformation

Purpose:
Clean raw orders, customers and products datasets.
"""

from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Clean customer master data."""

    print("Cleaning customers...")

    # Remove duplicate customer IDs
    df = df.drop_duplicates(
        subset="customer_id",
        keep="first"
    )

    # Standardize text columns
    text_columns = [
        "customer_name",
        "city",
        "state"
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # Standardize capitalization
    df["city"] = df["city"].str.title()
    df["state"] = df["state"].str.title()

    # Normalize email
    df["email"] = (
        df["email"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Invalid or missing emails -> NULL
    valid_email = df["email"].str.contains(
        r"^[\w\.-]+@[\w\.-]+\.\w+$",
        na=False
    )

    df.loc[~valid_email, "email"] = pd.NA

    # Convert signup date
    df["signup_date"] = pd.to_datetime(
        df["signup_date"],
        errors="coerce"
    )

    return df


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """Clean product master data."""

    print("Cleaning products...")

    # Remove duplicate product IDs
    df = df.drop_duplicates(
        subset="product_id",
        keep="first"
    )

    # Standardize product text
    df["product_name"] = (
        df["product_name"]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    df["category"] = (
        df["category"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    df["supplier"] = (
        df["supplier"]
        .astype("string")
        .str.strip()
    )

    # Convert price to numeric
    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    # Invalid prices -> NULL
    df.loc[df["unit_price"] <= 0, "unit_price"] = pd.NA

    # Convert stock quantity
    df["stock_quantity"] = pd.to_numeric(
        df["stock_quantity"],
        errors="coerce"
    )

    # Negative stock -> NULL
    df.loc[
        df["stock_quantity"] < 0,
        "stock_quantity"
    ] = pd.NA

    return df


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Clean retail orders."""

    print("Cleaning orders...")

    # Remove duplicate order IDs
    df = df.drop_duplicates(
        subset="order_id",
        keep="first"
    )

    # Standardize text
    df["payment_method"] = (
        df["payment_method"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    df["order_status"] = (
        df["order_status"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    # Convert dates
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # Convert numeric columns
    numeric_columns = [
        "quantity",
        "unit_price",
        "discount",
        "order_total"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Invalid quantities
    df.loc[df["quantity"] <= 0, "quantity"] = pd.NA

    # Invalid prices
    df.loc[df["unit_price"] <= 0, "unit_price"] = pd.NA

    # Invalid discounts
    df.loc[
        (df["discount"] < 0)
        | (df["discount"] > 1),
        "discount"
    ] = pd.NA

    # Recalculate order total
    df["order_total"] = (
        df["quantity"]
        * df["unit_price"]
        * (1 - df["discount"])
    ).round(2)

    return df


def main():

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Load raw data
    customers = pd.read_csv(
        RAW_DATA_DIR / "customers.csv"
    )

    products = pd.read_csv(
        RAW_DATA_DIR / "products.csv"
    )

    orders = pd.read_csv(
        RAW_DATA_DIR / "orders_raw.csv"
    )

    # Transform datasets
    customers_clean = clean_customers(customers)

    products_clean = clean_products(products)

    orders_clean = clean_orders(orders)

    # Save cleaned data
    customers_clean.to_csv(
        PROCESSED_DATA_DIR / "customers_clean.csv",
        index=False
    )

    products_clean.to_csv(
        PROCESSED_DATA_DIR / "products_clean.csv",
        index=False
    )

    orders_clean.to_csv(
        PROCESSED_DATA_DIR / "orders_clean.csv",
        index=False
    )

    print("\nCleaning completed successfully!")

    print("\nCleaned dataset sizes:")

    print("Customers:", customers_clean.shape)

    print("Products:", products_clean.shape)

    print("Orders:", orders_clean.shape)


if __name__ == "__main__":
    main()