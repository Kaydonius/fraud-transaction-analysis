-- overall fraud rate
SELECT
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_count,
    ROUND(AVG(isFraud * 100), 4) AS fraud_rate_percentage
FROM transaction_data;

-- fraud rate by transaction type
SELECT type,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_count,
    ROUND(AVG(isFraud * 100), 4) AS fraud_rate_percentage
FROM transaction_data
GROUP BY type;

-- fraud volume over time step
SELECT step, SUM(isfraud) AS fraud_count
FROM transaction_data
GROUP BY step;

-- avg transaction amount: fraud vs non fraud
SELECT ROUND(AVG(amount)) AS avg_amount, isfraud
FROM transaction_data
GROUP BY isfraud;

-- top origin accounts by fraud count
SELECT nameorig, SUM(isfraud) AS fraud_count
FROM transaction_data
GROUP BY nameorig
ORDER BY fraud_count DESC
LIMIT 10;

-- top destinations receiving fraudulent funds
SELECT namedest, 
    SUM(amount) AS total_fraud_amount,
    COUNT(*) AS fraud_count
FROM transaction_data
WHERE isfraud = 1
GROUP BY namedest
ORDER BY total_fraud_amount DESC
LIMIT 10;

-- transactions w/ balance inconsistencies (origin)
SELECT nameorig, namedest, oldbalanceorg, newbalanceorig, amount,
    oldbalanceorg - amount AS expected_new_balance,
    newbalanceorig - (oldbalanceorg - amount) AS discrepancy
FROM transaction_data
WHERE ABS(oldbalanceorg - amount - newbalanceorig) > 0.01
ORDER BY ABS(oldbalanceorg - amount - newbalanceorig) DESC;

-- fraud rate by transaction amount
SELECT 
    CASE
        WHEN amount < 1000 THEN 'Under 1K'
        WHEN amount < 10000 THEN '1K-10K'
        WHEN amount < 100000 THEN '10K-100K'
        WHEN amount < 1000000 THEN '100K-1M'
        ELSE '1M+'
    END AS amount_range,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_count,
    ROUND(AVG(isFraud * 100), 4) AS fraud_rate_percentage
FROM transaction_data
GROUP BY amount_range
ORDER BY MIN(amount);