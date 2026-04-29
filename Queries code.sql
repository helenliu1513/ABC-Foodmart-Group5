-- Query 1 - Total Sales by Store (Year 2025)
SELECT 
    s.store_name,
    SUM(st.total_amount) AS total_sales
FROM sales_transaction st
JOIN store s ON st.store_id = s.store_id
GROUP BY s.store_name;

-- Query 2 - Sales, Purchases, and Estimated Profit by Store

SELECT 
    s.store_name,
    SUM(CASE WHEN a.record_type = 'revenue' THEN a.amount ELSE 0 END) AS total_sales,
    SUM(CASE WHEN a.record_type = 'expense' THEN a.amount ELSE 0 END) AS total_purchases,
    SUM(CASE WHEN a.record_type = 'revenue' THEN a.amount ELSE 0 END)
    - SUM(CASE WHEN a.record_type = 'expense' THEN a.amount ELSE 0 END) AS estimated_profit
FROM accounting_record a
JOIN store s ON a.store_id = s.store_id
WHERE a.record_date >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY s.store_name
ORDER BY s.store_name;

-- Query 3: Top 10 Products by Sales

SELECT 
    pc.category_name,
    p.product_name,
    SUM(stl.line_total) AS total_sales
FROM sales_transaction_line stl
JOIN sales_transaction st ON stl.sale_id = st.sale_id
JOIN product p ON stl.product_id = p.product_id
JOIN product_category pc ON p.category_id = pc.category_id
WHERE st.sale_timestamp >= DATE '2025-01-01'
  AND st.sale_timestamp < DATE '2026-01-01'
GROUP BY pc.category_name, p.product_name
ORDER BY total_sales DESC
LIMIT 10;

-- Query 4: Vendors with Delayed Deliveries

SELECT 
    v.vendor_name,
    COUNT(d.delivery_id) AS total_deliveries,
    COUNT(*) FILTER (WHERE d.delivery_status = 'delayed') AS delayed_deliveries,
    ROUND(
        COUNT(*) FILTER (WHERE d.delivery_status = 'delayed') * 100.0 / COUNT(d.delivery_id), 2
    ) AS delay_percentage,
    ROUND(
        AVG(d.delay_days) FILTER (WHERE d.delivery_status = 'delayed'), 2
    ) AS avg_delay_days
FROM delivery d
JOIN vendor v ON d.vendor_id = v.vendor_id
GROUP BY v.vendor_name
ORDER BY delay_percentage DESC
LIMIT 10;

-- Query 5: Monthly Store Sales (Business Growth Trend)

SELECT
  st.store_id,
  s.store_name,
  DATE_TRUNC('month', st.sale_timestamp) AS month,
  SUM(st.total_amount) AS monthly_sales
FROM sales_transaction st
JOIN store s ON st.store_id = s.store_id
GROUP BY st.store_id, s.store_name, month
ORDER BY month, monthly_sales DESC;

-- Query 6: Employee Count and Salary Analysis by Store

SELECT 
    s.store_name,
    COUNT(e.employee_id) AS employee_count,
    ROUND(SUM(COALESCE(e.annual_salary, 0)), 2) AS total_annual_salary,
    ROUND(AVG(COALESCE(e.annual_salary, 0)), 2) AS avg_salary
FROM employee e
JOIN store s ON e.store_id = s.store_id
GROUP BY s.store_name
ORDER BY total_annual_salary DESC;

-- Query 7: Loyalty Customers vs. Walk-in Customers

SELECT 
    CASE 
        WHEN la.customer_id IS NOT NULL THEN 'Loyalty Customers'
        ELSE 'Walk-in Customers'
    END AS customer_type,
    COUNT(st.sale_id) AS total_transactions,
    ROUND(SUM(st.total_amount), 2) AS total_sales
FROM sales_transaction st
LEFT JOIN customer_loyalty_account la ON st.customer_id = la.customer_id
GROUP BY customer_type;

-- Query 8: Cash vs. Card Sales Across Stores

SELECT
    s.store_name,
    p.payment_method,
    COUNT(*) AS total_transactions,
    ROUND(SUM(p.payment_amount), 2) AS total_amount
FROM payment p
JOIN sales_transaction st ON p.sale_id = st.sale_id
JOIN store s ON st.store_id = s.store_id
GROUP BY s.store_name, p.payment_method
ORDER BY s.store_name, total_transactions DESC;

-- Query 9: Sales Distribution Across Days of the Week

SELECT
    s.store_name,
    TRIM(TO_CHAR(st.sale_timestamp, 'Day')) AS day_of_week,
    EXTRACT(DOW FROM st.sale_timestamp) AS day_order,
    SUM(st.total_amount) AS total_sales
FROM sales_transaction st
JOIN store s ON st.store_id = s.store_id
GROUP BY s.store_name, day_of_week, day_order
ORDER BY day_order, s.store_name;

-- Query 10: Top Performing Employees by Sales

SELECT
    e.first_name || ' ' || e.last_name AS employee_name,
    s.store_name,
    SUM(st.total_amount) AS total_sales
FROM sales_transaction st
JOIN employee e ON st.employee_id = e.employee_id
JOIN store s ON e.store_id = s.store_id
GROUP BY employee_name, s.store_name
ORDER BY total_sales DESC
LIMIT 10;
