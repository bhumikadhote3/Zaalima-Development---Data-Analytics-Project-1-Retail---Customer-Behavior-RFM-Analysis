USE online_sales_db;
GO

/* =========================
   1️⃣  DROP TABLES (if exist)
========================= */

IF OBJECT_ID('Fact_Sales', 'U') IS NOT NULL
    DROP TABLE Fact_Sales;

IF OBJECT_ID('Dim_Product', 'U') IS NOT NULL
    DROP TABLE Dim_Product;

IF OBJECT_ID('Dim_Date', 'U') IS NOT NULL
    DROP TABLE Dim_Date;
GO

/* =========================
   2️⃣  CREATE DIMENSION TABLES
========================= */

CREATE TABLE Dim_Date (
    date_id INT IDENTITY(1,1) PRIMARY KEY,
    order_date DATE
);

CREATE TABLE Dim_Product (
    product_id_key INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT
);
GO

/* =========================
   3️⃣  INSERT INTO DIM TABLES
========================= */

INSERT INTO Dim_Date (order_date)
SELECT DISTINCT CAST(order_date AS DATE)
FROM online_sales_orders;

INSERT INTO Dim_Product (product_id)
SELECT DISTINCT product_id
FROM online_sales_orders;
GO

/* =========================
   4️⃣  CREATE FACT TABLE
========================= */

CREATE TABLE Fact_Sales (
    sales_id INT IDENTITY(1,1) PRIMARY KEY,
    date_id INT,
    product_id_key INT,
    amount DECIMAL(10,2),

    FOREIGN KEY (date_id) REFERENCES Dim_Date(date_id),
    FOREIGN KEY (product_id_key) REFERENCES Dim_Product(product_id_key)
);
GO

/* =========================
   5️⃣  INSERT INTO FACT TABLE
========================= */

INSERT INTO Fact_Sales (date_id, product_id_key, amount)
SELECT 
    d.date_id,
    p.product_id_key,
    o.amount
FROM online_sales_orders o
JOIN Dim_Date d 
    ON CAST(o.order_date AS DATE) = d.order_date
JOIN Dim_Product p 
    ON o.product_id = p.product_id;
GO

/* =========================
   6️⃣  CREATE INDEXES
========================= */

CREATE INDEX idx_fact_date ON Fact_Sales(date_id);
CREATE INDEX idx_fact_product ON Fact_Sales(product_id_key);
GO

/* =========================
   7️⃣  VERIFY
========================= */

SELECT COUNT(*) AS Total_Fact_Rows FROM Fact_Sales;
SELECT COUNT(*) AS Total_Dates FROM Dim_Date;
SELECT COUNT(*) AS Total_Products FROM Dim_Product;
