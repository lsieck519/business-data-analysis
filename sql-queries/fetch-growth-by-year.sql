-- Open-ended question:
-- At what percent has Fetch grown year over year?

-- Calculating the number of new users each year

WITH 

yearly_user_counts AS (
    SELECT 
        strftime('%Y', created_date) AS year,
        COUNT(DISTINCT id) AS new_users
    FROM Users
    GROUP BY year
),

total_users AS (
    SELECT 
        year,
        SUM(new_users) OVER (ORDER BY year) AS total_users
    FROM yearly_user_counts
)

SELECT 
    y1.year,
    y1.new_users,
    COALESCE(y2.new_users, 0) AS prev_year_users,
    y1.new_users - COALESCE(y2.new_users, 0) AS user_growth,
    CASE
        WHEN y2.new_users = 0 THEN NULL 
        ELSE ROUND(((y1.new_users - y2.new_users) * 100.0) / y2.new_users, 2)  -- Growth percentage
    END AS growth_percentage,
    t.total_users
FROM yearly_user_counts y1
LEFT JOIN yearly_user_counts y2 
    ON CAST(y1.year AS INTEGER) = CAST(y2.year AS INTEGER) + 1
JOIN total_users t 
    ON y1.year = t.year
ORDER BY y1.year;