import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
orders = pd.read_csv("data/processed/orders_final.csv")
products = pd.read_csv("data/processed/products_clean.csv")

# Merge order data with product names
df = orders.merge(
    products[["product_id", "product_name"]],
    on="product_id",
    how="left"
)

# Calculate revenue per product
product_revenue = (
    df.groupby("product_name")["order_total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Reverse order for horizontal chart
product_revenue = product_revenue.sort_values(ascending=True)

# Create chart
plt.figure(figsize=(12, 7))

product_revenue.plot(kind="barh")

plt.title("Top 10 Products by Revenue", fontsize=16)
plt.xlabel("Total Revenue")
plt.ylabel("Product Name")
plt.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()

# Save chart
plt.savefig("outputs/charts/top_10_products.png", dpi=300)

# Display chart
plt.show()

# Print results
print("\nTop 10 Products by Revenue:")
print(product_revenue.sort_values(ascending=False))

print("\nTop products chart created successfully!")