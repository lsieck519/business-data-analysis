-- Open-ended question:
-- At what percent has Fetch grown year over year?

WITH yearly_user_counts AS (
    SELECT 
        strftime('%Y', created_date) AS year,
        COUNT(DISTINCT id) AS new_users
    FROM users
    GROUP BY year
)

SELECT 
    y1.year,
    y1.new_users,
    y2.new_users AS prev_year_users,
    y1.new_users - COALESCE(y2.new_users, 0) AS user_growth,
    ROUND(((y1.new_users - COALESCE(y2.new_users, 0)) / COALESCE(y2.new_users, 1)) * 100, 2) AS growth_percentage
FROM yearly_user_counts y1
LEFT JOIN yearly_user_counts y2 ON y1.year = strftime('%Y', date(y2.year || '-01-01', '-1 year'))
ORDER BY y1.year;

