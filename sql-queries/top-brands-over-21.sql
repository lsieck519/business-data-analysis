-- Closed-ended question: 
-- What are the top 5 brands by receipts scanned among users 21 and over?


with 

-- get IDs of users 21 and over
users_cte as (
    SELECT id  
    FROM Users 
    WHERE strftime('%Y', 'now') - strftime('%Y', substr(birth_date, 1, 10)) - 
      (strftime('%m-%d', 'now') < strftime('%m-%d', substr(birth_date, 1, 10))) >= 21
),

-- get barcodes only associated with users 21 and over
transactions_cte as (
    SELECT t.barcode
    FROM Transactions t
    WHERE t.user_id IN (SELECT id FROM users_cte)
    AND t.barcode IS NOT NULL
)

-- get top 5 brands by receipts scanned among users 21 and over
SELECT 
    p.brand,
    count(p.brand) as count 
FROM Products p
WHERE p.barcode in (SELECT barcode FROM transactions_cte)
AND p.brand != ""
GROUP BY p.brand
ORDER BY count DESC
LIMIT 5;
