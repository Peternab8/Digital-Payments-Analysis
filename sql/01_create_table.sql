-- Portfolio refresh: rebuildable SQLite schema for the verified cleaned CSV.
-- transaction_id is an internal surrogate key, not a source dataset column.
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    transaction_date TEXT NOT NULL, -- ISO 8601: YYYY-MM-DD HH:MM:SS
    product_category TEXT NOT NULL,
    product_name TEXT NOT NULL,
    merchant_name TEXT NOT NULL,
    product_amount REAL NOT NULL,
    transaction_fee REAL NOT NULL,
    cashback REAL NOT NULL,
    loyalty_points INTEGER NOT NULL,
    payment_method TEXT NOT NULL,
    transaction_status TEXT NOT NULL,
    merchant_id TEXT NOT NULL,
    device_type TEXT NOT NULL,
    location TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(product_category);
CREATE INDEX IF NOT EXISTS idx_transactions_method ON transactions(payment_method);
