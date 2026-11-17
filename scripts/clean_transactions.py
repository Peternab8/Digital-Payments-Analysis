"""Portfolio refresh (2026): reproducible cleaning of the supplied DEPI CSV.

Run: python scripts/clean_transactions.py
This is a cleaned-up pipeline based on the supplied original file and screenshots;
it is NOT a verbatim copy of the original 2024 Colab notebook.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/raw/modified_csv_with_problems.csv"
OUTPUT = ROOT / "data/processed/digital_payments_cleaned_verified.csv"

def main():
    df = pd.read_csv(SOURCE)
    original_rows = len(df)
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates().copy().reset_index(drop=True)

    # Map known categories by product, rather than overriding whole merchant categories.
    # A merchant can sell items in different categories (e.g. gifts AND online shopping).
    known = df.dropna(subset=["product_category"])
    unique_categories = known.groupby("product_name")["product_category"].nunique()
    ambiguous_products = unique_categories[unique_categories > 1]
    if not ambiguous_products.empty:
        raise ValueError("Ambiguous categories for products: " + ", ".join(ambiguous_products.index))
    category_mapping = known.groupby("product_name")["product_category"].first()
    df["product_category"] = df["product_category"].fillna(df["product_name"].map(category_mapping))

    # Mean imputation by product name, matching the documented 2024 approach.
    for col in ["product_amount", "transaction_fee"]:
        df[col] = df[col].fillna(df.groupby("product_name")[col].transform("mean"))
        df[col] = df[col].round(2)

    df["location"] = df["location"].fillna(df["location"].mode().iloc[0])
    df["payment_method"] = df["payment_method"].replace({"UPI": "Unified Payments Interface"})

    # ISO 8601 dates make sorting and SQLite reporting more reliable.
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], format="%m/%d/%Y %H:%M").dt.strftime("%Y-%m-%d %H:%M:%S")
    if df.isna().sum().sum():
        raise ValueError("Cleaning incomplete: null values remain.")
    if df.duplicated().sum():
        raise ValueError("Cleaning incomplete: duplicate rows remain.")
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(OUTPUT,index=False)
    print(f"Original rows: {original_rows}")
    print(f"Removed exact duplicate rows: {duplicates}")
    print(f"Verified output rows: {len(df)}")
    print(f"Output: {OUTPUT}")

if __name__ == "__main__":
    main()
