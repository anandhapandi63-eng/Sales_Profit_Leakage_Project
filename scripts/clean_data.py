import pandas as pd

# Correct file path from project root
file_path = "data/sample_superstore.csv"

# Load dataset
df = pd.read_csv(file_path, encoding="latin1")

print("Original Shape:", df.shape)

# Clean column names
df.columns = df.columns.str.strip()

# Remove duplicates
df.drop_duplicates(inplace=True)

# Convert date columns
for col in ["Order Date", "Ship Date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Fill missing values
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

obj_cols = df.select_dtypes(include="object").columns
for col in obj_cols:
    df[col] = df[col].fillna("Unknown")

# Add Profit Margin column
if "Sales" in df.columns and "Profit" in df.columns:
    df["Profit Margin %"] = (df["Profit"] / df["Sales"]) * 100

# Save cleaned dataset
output_path = "data/clean_superstore.csv"
df.to_csv(output_path, index=False)

print("Cleaned data saved successfully!")