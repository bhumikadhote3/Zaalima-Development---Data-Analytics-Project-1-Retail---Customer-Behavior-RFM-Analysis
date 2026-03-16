USE RetailDB;
GO

SELECT 
    fs.customer_key,
    MIN(dd.[date]) AS first_purchase_date
FROM dbo.Fact_Sales fs
INNER JOIN dbo.Dim_Date dd
    ON fs.date_key = dd.date_key
GROUP BY fs.customer_key
ORDER BY fs.customer_key;

USE RetailDB;
GO

SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Dim_Date';


USE RetailDB;
GO

SELECT 
    fs.customer_key,
    MIN(dd.order_date) AS first_purchase_date
FROM dbo.Fact_Sales fs
INNER JOIN dbo.Dim_Date dd
    ON fs.date_key = dd.date_key
GROUP BY fs.customer_key
ORDER BY fs.customer_key;

USE RetailDB;
GO

SELECT 
    fs.customer_key,
    FORMAT(MIN(dd.order_date), 'yyyy-MM') AS cohort_month
FROM dbo.Fact_Sales fs
JOIN dbo.Dim_Date dd
    ON fs.date_key = dd.date_key
GROUP BY fs.customer_key
ORDER BY fs.customer_key;

USE RetailDB;
GO

WITH FirstPurchase AS (
    SELECT 
        fs.customer_key,
        MIN(dd.order_date) AS first_purchase_date
    FROM dbo.Fact_Sales fs
    JOIN dbo.Dim_Date dd
        ON fs.date_key = dd.date_key
    GROUP BY fs.customer_key
)

SELECT 
    fp.customer_key,
    FORMAT(fp.first_purchase_date, 'yyyy-MM') AS cohort_month,
    FORMAT(dd.order_date, 'yyyy-MM') AS transaction_month,
    DATEDIFF(MONTH, fp.first_purchase_date, dd.order_date) AS month_number
FROM dbo.Fact_Sales fs
JOIN dbo.Dim_Date dd
    ON fs.date_key = dd.date_key
JOIN FirstPurchase fp
    ON fs.customer_key = fp.customer_key
ORDER BY fp.customer_key;

USE RetailDB;
GO

WITH FirstPurchase AS (
    SELECT 
        fs.customer_key,
        MIN(dd.order_date) AS first_purchase_date
    FROM dbo.Fact_Sales fs
    JOIN dbo.Dim_Date dd
        ON fs.date_key = dd.date_key
    GROUP BY fs.customer_key
),

CohortData AS (
    SELECT 
        fp.customer_key,
        FORMAT(fp.first_purchase_date, 'yyyy-MM') AS cohort_month,
        DATEDIFF(MONTH, fp.first_purchase_date, dd.order_date) AS month_number
    FROM dbo.Fact_Sales fs
    JOIN dbo.Dim_Date dd
        ON fs.date_key = dd.date_key
    JOIN FirstPurchase fp
        ON fs.customer_key = fp.customer_key
)

SELECT 
    cohort_month,
    month_number,
    COUNT(DISTINCT customer_key) AS customer_count
FROM CohortData
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number;


USE RetailDB;
GO

SELECT 
    s.sales_key,
    s.customer_key,
    s.product_key,
    p.product_name,
    s.quantity,
    s.revenue
FROM Fact_Sales s
JOIN Dim_Product p
    ON s.product_key = p.product_key

USE RetailDB;
GO

IF OBJECT_ID('dbo.vw_Sales_Product', 'V') IS NOT NULL
DROP VIEW dbo.vw_Sales_Product;
GO

CREATE VIEW dbo.vw_Sales_Product AS
SELECT 
    s.sales_key,
    s.customer_key,
    s.product_key,
    p.product_name,
    s.quantity,
    s.revenue,
    d.order_date,
    d.year,
    d.month,
    d.day
FROM dbo.Fact_Sales s
JOIN dbo.Dim_Product p
    ON s.product_key = p.product_key
JOIN dbo.Dim_Date d
    ON s.date_key = d.date_key;
GO