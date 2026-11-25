# Retail Data Engineering Pipeline 2027

**An end-to-end Retail Data Engineering and Analytics Project using Python, Pandas, MySQL, SQL, and Streamlit.**

## Project Overview

This project demonstrates an end-to-end data engineering workflow for a retail business. It transforms raw and inconsistent retail data into clean, validated datasets, loads the data into a MySQL data warehouse, performs SQL-based business analysis, and creates interactive visualizations using Python and Streamlit.

The project focuses on building a reliable data pipeline while generating meaningful business insights from retail sales data.

## Project Objectives

- Build an end-to-end ETL pipeline.
- Perform data exploration and data cleaning.
- Identify and quarantine invalid records.
- Validate data quality and consistency.
- Load processed datasets into MySQL.
- Perform business analytics using SQL.
- Develop interactive charts and dashboards.
- Maintain project code using Git and GitHub.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and ETL |
| Pandas | Data manipulation and cleaning |
| MySQL | Data warehouse |
| SQL | Business analytics |
| Matplotlib | Static visualizations |
| Seaborn | Data visualization |
| Plotly | Interactive charts |
| Streamlit | Interactive dashboard |
| Git & GitHub | Version control |

## Project Architecture

```text
Raw Retail Data
       |
       v
Data Exploration
       |
       v
Data Cleaning
       |
       v
Data Validation
       |
       v
Data Quarantine
       |
       v
Final Dataset Creation
       |
       v
MySQL Data Warehouse
       |
       v
SQL Business Analytics
       |
       v
Python Visualizations
       |
       v
Interactive Streamlit Dashboard
```

## Project Structure

```text
retail-data-engineering-pipeline-2027/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── orders_raw.csv
│   │   └── products.csv
│   │
│   └── processed/
│       ├── customers_clean.csv
│       ├── products_clean.csv
│       ├── orders_clean.csv
│       ├── orders_final.csv
│       ├── data_quality_report.csv
│       └── rejected_orders_*.csv
│
├── outputs/
│   └── charts/
│
├── src/
│   ├── transform/
│   ├── load/
│   └── visualization/
│       ├── monthly_revenue.py
│       ├── category_revenue.py
│       ├── order_status.py
│       ├── top_products.py
│       ├── monthly_orders.py
│       └── dashboard.py
│
├── sql/
├── tests/
├── docs/
└── README.md
```

## ETL Pipeline

### 1. Data Exploration
- Examined raw customer, product, and order datasets.
- Identified missing values and inconsistent records.
- Explored dataset structure and relationships.

### 2. Data Cleaning
- Cleaned customer information.
- Cleaned product information.
- Standardized order data.
- Checked invalid dates, quantities, prices, and discounts.

### 3. Data Validation and Quarantine
- Identified missing customer references.
- Identified missing product references.
- Detected invalid quantities, prices, discounts, and dates.
- Separated rejected records into quarantine files.

### 4. Final Dataset Creation

Generated validated datasets for further processing and analytics.

**Data Quality Results**

| Metric | Records |
|---|---:|
| Original Orders | 1,499 |
| Valid Orders | 1,449 |
| Rejected Orders | 50 |
| Clean Customers | 219 |
| Clean Products | 59 |

All final dataset validation checks passed.

## MySQL Data Warehouse

Database: `retail_data_warehouse`

Tables:

- customers
- products
- orders

The processed datasets were loaded into MySQL using Python and MySQL Connector.

**Successful loading results:**

| Table | Records |
|---|---:|
| Customers | 219 |
| Products | 59 |
| Orders | 1,449 |

Referential integrity was checked, and the orphan order validation returned zero records.

## SQL Business Analytics

SQL analysis was performed to generate business insights.

**Key Results**

| Business Metric | Result |
|---|---:|
| Total Revenue | 29,554,508.45 |
| Average Order Value | 20,396.49 |
| Total Orders | 1,449 |

**Revenue by Category**

| Category | Revenue |
|---|---:|
| Beauty | 7,586,504.43 |
| Clothing | 4,910,610.16 |
| Home & Kitchen | 4,696,942.82 |
| Electronics | 4,652,644.85 |
| Sports | 4,203,469.27 |
| Books | 3,504,336.92 |

Beauty generated the highest revenue among the product categories.

## Data Visualization and Dashboard

Five visualizations were developed using Python.

1. Monthly Revenue Trend
2. Revenue by Product Category
3. Order Status Distribution
4. Top 10 Products by Revenue
5. Monthly Order Volume

Chart images are stored in:

`outputs/charts/`

An interactive dashboard was developed using Streamlit and Plotly.

**Dashboard Features**

- Total Revenue KPI
- Total Orders KPI
- Average Order Value KPI
- Delivered Orders KPI
- Date range filter
- Monthly revenue analysis
- Category-wise revenue analysis
- Order status distribution
- Top 10 products by revenue
- Monthly order volume
- Order data table

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/khangulnaaz/retail-data-engineering-pipeline-2027.git
```

### 2. Navigate to the project

```bash
cd retail-data-engineering-pipeline-2027
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the environment (Mac/Linux)

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install pandas matplotlib seaborn plotly streamlit mysql-connector-python
```

### 6. Configure MySQL

Install and start MySQL, then create the database:

```sql
CREATE DATABASE retail_data_warehouse;
```

Configure your MySQL credentials securely using environment variables. Never upload passwords or secrets to GitHub.

## Running the Project

### Run the data exploration script

```bash
python src/explore_data.py
```

### Run the data cleaning and validation scripts

```bash
python src/transform/clean_data.py
python src/transform/validate_cleaned_data.py
python src/transform/quarantine_data.py
python src/transform/create_final_dataset.py
python src/transform/validate_final_dataset.py
```

### Load data into MySQL

```bash
python src/load/load_to_mysql.py
```

### Generate visualizations

```bash
python src/visualization/monthly_revenue.py
python src/visualization/category_revenue.py
python src/visualization/order_status.py
python src/visualization/top_products.py
python src/visualization/monthly_orders.py
```

### Launch the interactive dashboard

```bash
streamlit run src/visualization/dashboard.py
```

## Key Learnings

Through this project, I gained practical experience in:

- Building Python-based ETL pipelines.
- Handling real-world-style data quality issues.
- Implementing data validation and quarantine processes.
- Working with relational databases and MySQL.
- Writing SQL queries for business analytics.
- Developing interactive dashboards.
- Maintaining code using Git and GitHub.

## Future Improvements

- Implement automated incremental data loading.
- Add comprehensive automated unit tests.
- Introduce pipeline scheduling.
- Add more advanced customer analytics.
- Deploy the interactive dashboard online.

## Author

**Gulnaaz Khan**

MBA – Operations Management  
BCA Graduate

**GitHub Repository:**  
https://github.com/khangulnaaz/retail-data-engineering-pipeline-2027

---

*This project was developed as a Data Engineering portfolio project to demonstrate practical skills in ETL development, data quality management, database operations, SQL analytics, and business intelligence.*
