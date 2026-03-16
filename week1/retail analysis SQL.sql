-- ===============================================
-- 1. Drop existing tables safely
-- Fact table first, then dimensions
-- ===============================================
IF OBJECT_ID('dbo.Fact_Sales', 'U') IS NOT NULL
    DROP TABLE dbo.Fact_Sales;
GO

IF OBJECT_ID('dbo.Dim_Customer', 'U') IS NOT NULL
    DROP TABLE dbo.Dim_Customer;
GO

IF OBJECT_ID('dbo.Dim_Product', 'U') IS NOT NULL
    DROP TABLE dbo.Dim_Product;
GO

IF OBJECT_ID('dbo.Dim_Date', 'U') IS NOT NULL
    DROP TABLE dbo.Dim_Date;
GO

IF OBJECT_ID('dbo.Retail_Cleaned', 'U') IS NOT NULL
    DROP TABLE dbo.Retail_Cleaned;
GO

-- ===============================================
-- 2. Use existing database
-- ===============================================
USE [RetailDB];
GO

-- ===============================================
-- 3. Preview Raw Data
-- ===============================================
SELECT TOP 10 * 
FROM RETAIL;
GO

-- ===============================================
-- 4. Create Cleaned Staging Table
-- ===============================================
SELECT
    TXN_ID                 AS order_id,
    LYLTY_CARD_NBR         AS customer_id,
    PROD_NBR               AS product_id,
    PROD_NAME              AS product_name,
    CAST([DATE] AS DATE)   AS order_date,
    PROD_QTY               AS quantity,
    UNIT_PRICE             AS unit_price,
    PROD_QTY * UNIT_PRICE  AS revenue,
    STORE_NBR              AS store_id
INTO Retail_Cleaned
FROM RETAIL
WHERE LYLTY_CARD_NBR IS NOT NULL
  AND PROD_QTY > 0
  AND UNIT_PRICE > 0
  AND TOT_SALES > 0;
GO

-- ===============================================
-- 5. Validate Cleaned Data
-- ===============================================
SELECT COUNT(*) AS total_rows
FROM Retail_Cleaned;
GO

SELECT COUNT(*) AS invalid_revenue_rows
FROM Retail_Cleaned
WHERE revenue <= 0;
GO

-- ===============================================
-- 6. Create Dimension Tables
-- ===============================================

-- Dim_Customer
CREATE TABLE Dim_Customer (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL
);
GO

INSERT INTO Dim_Customer (customer_id)
SELECT DISTINCT customer_id
FROM Retail_Cleaned;
GO

-- Dim_Product
CREATE TABLE Dim_Product (
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(255),
    unit_price DECIMAL(10,2)
);
GO

INSERT INTO Dim_Product (product_id, product_name, unit_price)
SELECT DISTINCT product_id, product_name, unit_price
FROM Retail_Cleaned;
GO

-- Dim_Date
CREATE TABLE Dim_Date (
    date_key INT IDENTITY(1,1) PRIMARY KEY,
    order_date DATE,
    [year] INT,
    [month] INT,
    [day] INT
);
GO

INSERT INTO Dim_Date (order_date, [year], [month], [day])
SELECT DISTINCT
    order_date,
    YEAR(order_date),
    MONTH(order_date),
    DAY(order_date)
FROM Retail_Cleaned;
GO

-- ===============================================
-- 7. Create Fact Table
-- ===============================================
CREATE TABLE Fact_Sales (
    sales_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_key INT,
    product_key INT,
    date_key INT,
    quantity INT,
    revenue DECIMAL(12,2),
    FOREIGN KEY (customer_key) REFERENCES Dim_Customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES Dim_Product(product_key),
    FOREIGN KEY (date_key) REFERENCES Dim_Date(date_key)
);
GO

-- ===============================================
-- 8. Load Fact Table
-- ===============================================
INSERT INTO Fact_Sales (customer_key, product_key, date_key, quantity, revenue)
SELECT
    c.customer_key,
    p.product_key,
    d.date_key,
    r.quantity,
    r.revenue
FROM Retail_Cleaned r
JOIN Dim_Customer c ON r.customer_id = c.customer_id
JOIN Dim_Product p ON r.product_id = p.product_id
JOIN Dim_Date d ON r.order_date = d.order_date;
GO

-- ===============================================
-- 9. Create Indexes for Performance
-- ===============================================
CREATE INDEX idx_fact_customer ON Fact_Sales(customer_key);
CREATE INDEX idx_fact_product ON Fact_Sales(product_key);
CREATE INDEX idx_fact_date ON Fact_Sales(date_key);
GO

-- ===============================================
-- 10. Analytical Queries
-- ===============================================

-- Total Revenue
SELECT SUM(revenue) AS total_revenue
FROM Fact_Sales;
GO

-- Revenue by Date
SELECT
    d.order_date,
    SUM(f.revenue) AS total_revenue
FROM Fact_Sales f
JOIN Dim_Date d ON f.date_key = d.date_key
GROUP BY d.order_date
ORDER BY d.order_date;
GO

-- Top 10 Products by Revenue
SELECT TOP 10
    p.product_name,
    SUM(f.revenue) AS total_revenue
FROM Fact_Sales f
JOIN Dim_Product p ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY total_revenue DESC;
GO

-- Top 10 Customers by Revenue
SELECT TOP 10
    c.customer_id,
    SUM(f.revenue) AS total_revenue
FROM Fact_Sales f
JOIN Dim_Customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_id
ORDER BY total_revenue DESC;
GO

-- Average Daily Revenue
SELECT AVG(daily_revenue) AS avg_daily_revenue
FROM (
    SELECT
        d.order_date,
        SUM(f.revenue) AS daily_revenue
    FROM Fact_Sales f
    JOIN Dim_Date d ON f.date_key = d.date_key
    GROUP BY d.order_date
) t;
GO