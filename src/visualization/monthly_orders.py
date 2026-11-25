import pandas as pd
import matplotlib.pyplot as plt

# Load final cleaned dataset
df = pd.read_csv("data/processed/orders_final.csv")

# Convert order_date to datetime
df["order_date"] = pd.to_datetime(df["order_date"])

# Extract month
df["month"] = df["order_date"].dt.to_period("M")

# Calculate monthly order count
monthly_orders = (
    df.groupby("month")["order_id"]
    .count()
    .reset_index(name="order_count")
)

monthly_orders["month"] = monthly_orders["month"].astype(str)

# Create line chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_orders["month"],
    monthly_orders["order_count"],
    marker="o"
)

plt.title("Monthly Order Volume", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Save chart
plt.savefig("outputs/charts/monthly_orders.png", dpi=300)

# Display chart
plt.show()

# Print results
print("\nMonthly Order Volume:")
print(monthly_orders)

print("\nMonthly order chart created successfully!")