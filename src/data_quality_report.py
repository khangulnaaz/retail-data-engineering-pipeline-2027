"""
Retail Data Engineering Pipeline
Data Quality Assessment

Purpose:
Identify missing values, duplicates and invalid records
in raw retail datasets.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
REPORT_DIR = PROJECT_ROOT / "data" / "processed"


def analyze_data_quality(file_path: Path) -> pd.DataFrame:

    df = pd.read_csv(file_path)

    report = pd.DataFrame({
        "column_name": df.columns,
        "data_type": df.dtypes.astype(str).values,
        "total_rows": len(df),
        "missing_values": df.isnull().sum().values,
        "missing_percentage": (
            df.isnull().sum().values / len(df) * 100
        ).round(2),
        "unique_values": df.nunique().values,
    })

    report["duplicate_rows"] = df.duplicated().sum()

    print(f"\n{'=' * 60}")
    print(f"DATA QUALITY REPORT: {file_path.name}")
    print("=" * 60)

    print(report.to_string(index=False))

    return report


def main():

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    datasets = [
        "orders_raw.csv",
        "customers.csv",
        "products.csv",
    ]

    all_reports = []

    for dataset in datasets:

        file_path = RAW_DATA_DIR / dataset

        if not file_path.exists():
            print(f"File missing: {dataset}")
            continue

        report = analyze_data_quality(file_path)

        report["dataset_name"] = dataset

        all_reports.append(report)

    if all_reports:

        final_report = pd.concat(
            all_reports,
            ignore_index=True
        )

        output_path = REPORT_DIR / "data_quality_report.csv"

        final_report.to_csv(output_path, index=False)

        print("\nData quality report saved successfully!")
        print(f"Location: {output_path}")


if __name__ == "__main__":
    main()