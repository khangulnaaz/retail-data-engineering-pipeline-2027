import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
orders = pd.read_csv("data/processed/orders_final.csv")
products = pd.read_csv("data/processed/products_clean.csv")

# Merge orders with product information
df = orders.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
)

# Calculate revenue by category
category_revenue = (
    df.groupby("category")["order_total"]
    .sum()
    .sort_values(ascending=False)
)

# Create bar chart
plt.figure(figsize=(10, 6))

category_revenue.plot(kind="bar")

plt.title("Revenue by Product Category", fontsize=16)
plt.xlabel("Product Category")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()

# Save chart
plt.savefig("outputs/charts/category_revenue.png", dpi=300)

# Display chart
plt.show()

# Print results
print("\nRevenue by Product Category:")
print(category_revenue)

print("\nCategory revenue chart created successfully!")