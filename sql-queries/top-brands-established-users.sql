-- Closed-ended question: 
-- What are the top 5 brands by sales among users that have had their account for at least six months?


with 

-- get IDs of users that have had their account for at least six months
users_cte as (
    SELECT ID  
    FROM Users 
    WHERE strftime('%Y-%m-%d', CREATED_DATE) < date('now', '-6 months')
),

-- get barcodes only associated with users that have had their account for at least six months
transactions_cte as (
    SELECT t.barcode
    FROM Transactions t
    WHERE t.user_id IN (SELECT id FROM users_cte)
    AND t.barcode IS NOT NULL
)

-- get top 5 brands by sales among users that have had their account for at least six months
SELECT 
    p.brand,
    count(p.brand) as count
FROM Products p
WHERE p.barcode in (SELECT barcode FROM transactions_cte)
AND p.brand != ""
GROUP BY p.brand
ORDER BY count DESC 
LIMIT 5;
