-- Advertising revenue by product and month (SQLite)
SELECT substr(start_date,1,7) month, product, SUM(booked_revenue) booked_revenue
FROM campaigns GROUP BY month,product ORDER BY month,product;
-- Digital click-through rate, excluding print
SELECT 100.0*SUM(clicks)/NULLIF(SUM(impressions),0) AS digital_ctr_pct
FROM campaigns WHERE product <> 'Print';
