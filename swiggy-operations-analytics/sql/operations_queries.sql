-- Assumed table: delivery_orders
SELECT hub, COUNT(*) AS total_orders,
       SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) AS completed_orders,
       ROUND(100.0*SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END)/NULLIF(COUNT(*),0),2) AS cancellation_rate_pct,
       ROUND(AVG(CASE WHEN status='Completed' THEN delivery_minutes END),2) AS avg_delivery_minutes,
       ROUND(100.0*SUM(CASE WHEN status='Completed' AND delivery_minutes<=promised_minutes THEN 1 ELSE 0 END)
         /NULLIF(SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END),0),2) AS on_time_rate_pct,
       ROUND(AVG(estimated_cost_inr),2) AS avg_estimated_cost_inr,
       ROUND(AVG(customer_rating),2) AS avg_customer_rating
FROM delivery_orders GROUP BY hub ORDER BY cancellation_rate_pct DESC;

-- Peak-hour cancellation analysis
SELECT hub, order_hour, COUNT(*) AS total_orders,
       SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END) AS cancellations
FROM delivery_orders GROUP BY hub, order_hour
HAVING COUNT(*) >= 20 ORDER BY cancellations DESC;

-- Late completed orders for root-cause investigation
SELECT order_id, hub, order_hour, delivery_minutes, promised_minutes, estimated_cost_inr
FROM delivery_orders WHERE status='Completed' AND delivery_minutes>promised_minutes
ORDER BY delivery_minutes-promised_minutes DESC;
