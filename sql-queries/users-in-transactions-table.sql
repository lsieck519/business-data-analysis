-- The results for the "top brands" queries weren't quite looking right
-- So I wanted to write this query to see how much relevant data we have
-- Limited results may explain why the top brands query is returning results with very low counts

WITH 

-- Narrowing down to ALL users that are in the transactions table
users_in_transactions_cte AS (
    SELECT DISTINCT u.ID 
    FROM Users u
    JOIN Transactions t 
    ON u.ID = t.USER_ID
),

-- Narrowing down to ALL transactions that have a barcode in the products table
transactions_cte AS (
    SELECT t.USER_ID, t.barcode
    FROM Transactions t
    JOIN Products p 
    ON t.barcode = p.barcode
),

-- Getting brands that can be linked to transactions table by barcode
brands_cte AS (
    SELECT p.brand, p.barcode
    FROM Products p
    JOIN Transactions t 
    ON p.barcode = t.barcode
    JOIN users_in_transactions_cte u 
    ON t.USER_ID = u.ID
)

-- Joining CTEs to get associated brands with users in transactions table by barcode
SELECT DISTINCT
    u.ID AS user_in_transactions,
    t.USER_ID AS user_with_barcode_in_products,
    b.brand,
    b.barcode
FROM users_in_transactions_cte u
LEFT JOIN transactions_cte t 
ON u.ID = t.USER_ID
JOIN brands_cte b 
ON t.barcode = b.barcode
WHERE b.brand IS NOT NULL AND b.brand != '';
