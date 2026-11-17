"""Build a fresh SQLite database using the verified, cleaned DEPI dataset.
Run: python scripts/build_database.py
"""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data/processed/digital_payments_cleaned_verified.csv"
DB_PATH = ROOT / "database/digital_payments_verified.db"
SCHEMA_PATH = ROOT / "sql/01_create_table.sql"
COLUMNS = ["user_id", "transaction_date", "product_category", "product_name", "merchant_name",
           "product_amount", "transaction_fee", "cashback", "loyalty_points", "payment_method",
           "transaction_status", "merchant_id", "device_type", "location"]

def main():
    df = pd.read_csv(CSV_PATH)
    assert list(df.columns) == COLUMNS
    assert not df.isna().any().any()
    assert not df.duplicated().any()
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    if DB_PATH.exists(): DB_PATH.unlink()
    with sqlite3.connect(DB_PATH) as con:
        con.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        placeholders = ", ".join("?" for _ in COLUMNS)
        field_names = ", ".join(COLUMNS)
        con.executemany(f"INSERT INTO transactions ({field_names}) VALUES ({placeholders})",
                        list(df.itertuples(index=False,name=None)))
        result = con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
        assert result == len(df), (result, len(df))
        assert con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0] == 4999
    print(f"Created {DB_PATH} with {len(df)} rows")

if __name__ == "__main__":
    main()
