import pandas as pd
import matplotlib.pyplot as plt

# Load final cleaned dataset
df = pd.read_csv("data/processed/orders_final.csv")

# Count orders by status
status_counts = df["order_status"].value_counts()

# Create pie chart
plt.figure(figsize=(8, 8))

plt.pie(
    status_counts,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Order Status Distribution", fontsize=16)

plt.tight_layout()

# Save chart
plt.savefig("outputs/charts/order_status_distribution.png", dpi=300)

# Display chart
plt.show()

# Print results
print("\nOrders by Status:")
print(status_counts)

print("\nOrder status chart created successfully!")