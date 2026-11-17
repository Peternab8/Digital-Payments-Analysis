-- Portfolio refresh: example SQLite analysis queries.
-- Run these in DB Browser for SQLite against database/digital_payments_verified.db.
-- These queries were prepared for the GitHub portfolio and were not copied
-- from original 2024 SQL screenshots.

-- 1. Row count and transaction status breakdown
SELECT transaction_status, COUNT(*) AS transaction_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM transactions), 2) AS pct_of_all
FROM transactions
GROUP BY transaction_status
ORDER BY transaction_count DESC;

-- 2. Count of transactions per payment method
SELECT payment_method, COUNT(*) AS transaction_count
FROM transactions
GROUP BY payment_method
ORDER BY transaction_count DESC;

-- 3. Top categories by transaction volume
SELECT product_category, COUNT(*) AS transaction_count,
       ROUND(SUM(product_amount), 2) AS total_amount
FROM transactions
GROUP BY product_category
ORDER BY transaction_count DESC;

-- 4. Monthly transaction trend (all statuses)
SELECT substr(transaction_date, 1, 7) AS year_month,
       COUNT(*) AS transaction_count,
       ROUND(SUM(product_amount), 2) AS total_amount
FROM transactions
GROUP BY substr(transaction_date, 1, 7)
ORDER BY year_month;

-- 5. Success rates by payment method
SELECT payment_method,
       COUNT(*) AS all_transactions,
       SUM(CASE WHEN transaction_status = 'Successful' THEN 1 ELSE 0 END) AS successful_transactions,
       ROUND(100.0 * SUM(CASE WHEN transaction_status = 'Successful' THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_rate_pct
FROM transactions
GROUP BY payment_method
ORDER BY success_rate_pct DESC;

-- 6. Top merchants by transaction count
SELECT merchant_name, COUNT(*) AS transaction_count,
       ROUND(SUM(product_amount), 2) AS total_amount
FROM transactions
GROUP BY merchant_name
ORDER BY transaction_count DESC
LIMIT 10;

-- 7. Device distribution
SELECT device_type, COUNT(*) AS transaction_count
FROM transactions
GROUP BY device_type
ORDER BY transaction_count DESC;

-- 8. Location distribution
SELECT location, COUNT(*) AS transaction_count
FROM transactions
GROUP BY location
ORDER BY transaction_count DESC;

-- 9. Transaction fees and cashback by payment method
SELECT payment_method, COUNT(*) AS transaction_count,
       ROUND(AVG(transaction_fee), 2) AS avg_transaction_fee,
       ROUND(AVG(cashback), 2) AS avg_cashback
FROM transactions
GROUP BY payment_method
ORDER BY transaction_count DESC;
