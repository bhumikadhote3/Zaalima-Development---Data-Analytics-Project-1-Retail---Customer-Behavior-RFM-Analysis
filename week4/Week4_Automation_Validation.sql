-- Step 1: Check latest sales in Fact table
SELECT TOP 5 *
FROM dbo.Fact_Sales
ORDER BY sales_key DESC;

-- Step 2: Check view reflects latest data
SELECT TOP 5 *
FROM dbo.vw_Sales_Product
ORDER BY sales_key DESC;

-- Step 3: Insert test transaction
INSERT INTO dbo.Fact_Sales
(customer_key, product_key, date_key, quantity, revenue)
VALUES (1, 1, 1, 1, 500);

-- Step 4: Recheck view update
SELECT TOP 5 *
FROM dbo.vw_Sales_Product
ORDER BY sales_key DESC;