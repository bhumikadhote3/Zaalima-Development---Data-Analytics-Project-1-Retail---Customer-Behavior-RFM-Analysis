USE online_sales_db;
Go
    
-- 1?? Total Sales
SELECT SUM(amount) AS Total_Sales
FROM Fact_Sales;
GO
    
-- 2?? Sales by Date
SELECT 
    d.order_date,
    SUM(f.amount) AS Total_Sales
FROM Fact_Sales f
JOIN Dim_Date d ON f.date_id = d.date_id
GROUP BY d.order_date
ORDER BY d.order_date;
Go
    
-- 3?? Sales by Product
SELECT 
    p.product_id,
    SUM(f.amount) AS Total_Sales
FROM Fact_Sales f
JOIN Dim_Product p ON f.product_id_key = p.product_id_key
GROUP BY p.product_id
ORDER BY Total_Sales DESC;
Go
    
-- 4?? Top Selling Product
SELECT TOP 1
    p.product_id,
    SUM(f.amount) AS Total_Sales
FROM Fact_Sales f
JOIN Dim_Product p ON f.product_id_key = p.product_id_key
GROUP BY p.product_id
ORDER BY Total_Sales DESC;
Go
    
-- 5?? Average Daily Sales
SELECT 
    AVG(Daily_Sales) AS Avg_Daily_Sales
FROM (
    SELECT 
        d.order_date,
        SUM(f.amount) AS Daily_Sales
    FROM Fact_Sales f
    JOIN Dim_Date d ON f.date_id = d.date_id
    GROUP BY d.order_date
) AS DailySummary;
