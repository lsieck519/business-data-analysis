-- Closed-ended question: 
-- What are the top 5 brands by sales among users that have had their account for at least six months?

-- I thought about getting the top brands by sale $ amount but still a bit unclear on what the sales and quantity columns represent.
-- I'm assuming the barcode linking products and transactions is the barcode for the receipt itself and not specific products.
-- Presently, I am working under the assumption that quantity and sale refer to the entire receipt and not individual products.
-- This would be a situation where I send a quick Slack message for clarification!
-- Considering the above, I'll get the top brands by sales count instead

WITH 
users_cte AS (
    SELECT ID  
    FROM Users 
    WHERE strftime('%Y-%m-%d', CREATED_DATE) < date('now', '-6 months')
),
transactions_cte AS (
    SELECT DISTINCT t.barcode
    FROM Transactions t
    JOIN users_cte u ON t.user_id = u.ID
    WHERE t.barcode IS NOT NULL AND t.barcode != ''
)
SELECT 
    p.brand,
    COUNT(p.brand) AS count
FROM Products p
JOIN transactions_cte t ON p.barcode = t.barcode
WHERE p.brand IS NOT NULL AND p.brand != ''
GROUP BY p.brand
ORDER BY count DESC 
LIMIT 5;
