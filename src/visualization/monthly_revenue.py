import pandas as pd
import matplotlib.pyplot as plt

# Load final cleaned dataset
df = pd.read_csv("data/processed/orders_final.csv")

# Convert order_date to datetime
df["order_date"] = pd.to_datetime(df["order_date"])

# Calculate monthly revenue
df["month"] = df["order_date"].dt.to_period("M")

monthly_revenue = (
    df.groupby("month")["order_total"]
    .sum()
    .reset_index()
)

monthly_revenue["month"] = monthly_revenue["month"].astype(str)

# Create chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue["month"],
    monthly_revenue["order_total"],
    marker="o"
)

plt.title("Monthly Revenue Trend", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Save chart
plt.savefig("outputs/charts/monthly_revenue.png", dpi=300)

# Display chart
plt.show()

print("Monthly revenue chart created successfully!")
print(monthly_revenue)