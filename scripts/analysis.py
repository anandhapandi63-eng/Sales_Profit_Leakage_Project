import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --------------------------
# Setup
# --------------------------
sns.set_theme(style="whitegrid")
os.makedirs("visuals", exist_ok=True)

df = pd.read_csv("data/clean_superstore.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# Remove invalid dates
df = df.dropna(subset=["Order Date"])

# Add Margin
df["Profit Margin %"] = (df["Profit"] / df["Sales"]) * 100

# ==========================
# 1. Loss Making Categories
# ==========================
loss = df.groupby("Sub-Category")["Profit"].sum()
loss = loss[loss < 0].sort_values()

plt.figure(figsize=(10,6))
sns.barplot(x=loss.values, y=loss.index, palette="Reds_r")
plt.title("Loss-Making Sub-Categories")
plt.xlabel("Total Loss")
plt.ylabel("")
plt.tight_layout()
plt.savefig("visuals/01_loss_categories.png", dpi=300)
plt.close()

# ==========================
# 2. Profit by Region
# ==========================
region = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
sns.barplot(x=region.index, y=region.values, palette="Blues_d")
plt.title("Profit by Region")
plt.xlabel("")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("visuals/02_profit_region.png", dpi=300)
plt.close()

# ==========================
# 3. Discount vs Margin
# ==========================
disc = df.groupby("Discount")["Profit Margin %"].mean().reset_index()

plt.figure(figsize=(8,5))
sns.lineplot(data=disc, x="Discount", y="Profit Margin %", marker="o")
plt.title("Average Margin by Discount Level")
plt.xlabel("Discount")
plt.ylabel("Avg Profit Margin %")
plt.tight_layout()
plt.savefig("visuals/03_discount_margin.png", dpi=300)
plt.close()

# ==========================
# 4. Monthly Sales Trend
# ==========================
monthly = df.resample("M", on="Order Date")["Sales"].sum()

plt.figure(figsize=(12,5))
monthly.plot(linewidth=3)
plt.title("Monthly Sales Trend")
plt.xlabel("")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("visuals/04_sales_trend.png", dpi=300)
plt.close()

# ==========================
# 5. Category Sales
# ==========================
cat = df.groupby("Category")["Sales"].sum().sort_values()

plt.figure(figsize=(8,5))
sns.barplot(x=cat.values, y=cat.index, palette="viridis")
plt.title("Sales by Category")
plt.xlabel("Sales")
plt.ylabel("")
plt.tight_layout()
plt.savefig("visuals/05_category_sales.png", dpi=300)
plt.close()

print("Professional charts created successfully.")