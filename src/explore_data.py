"""
Retail Data Engineering Pipeline
Dataset exploration script.

Author: Gulnaaz Khan
Purpose: Explore raw retail CSV datasets.
"""

from pathlib import Path

import pandas as pd


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw dataset directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def explore_dataset(file_path: Path) -> None:
    """Read a CSV file and display basic dataset information."""

    print("\n" + "=" * 60)
    print(f"DATASET: {file_path.name}")
    print("=" * 60)

    # Read CSV file
    df = pd.read_csv(file_path)

    # Dataset dimensions
    print(f"\nShape: {df.shape}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # Column names
    print("\nColumn Names:")
    print(df.columns.tolist())

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Duplicate rows
    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    # First five records
    print("\nFirst Five Records:")
    print(df.head())


def main() -> None:
    """Explore all raw CSV files."""

    files = [
        RAW_DATA_DIR / "orders_raw.csv",
        RAW_DATA_DIR / "customers.csv",
        RAW_DATA_DIR / "products.csv",
    ]

    for file_path in files:
        if file_path.exists():
            explore_dataset(file_path)
        else:
            print(f"File not found: {file_path}")


if __name__ == "__main__":
    main()