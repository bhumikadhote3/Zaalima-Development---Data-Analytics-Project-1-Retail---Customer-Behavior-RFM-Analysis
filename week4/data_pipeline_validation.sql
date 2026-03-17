SELECT TOP 5 *
FROM dbo.Fact_Sales
ORDER BY sales_key DESC;

SELECT TOP 5 *
FROM dbo.vw_Sales_Product
ORDER BY sales_key DESC;

SELECT TOP 1 *
FROM dbo.Fact_Sales;

INSERT INTO dbo.Fact_Sales
(customer_key, product_key, date_key, quantity, revenue)
VALUES (1, 1, 1, 1, 500);

SELECT TOP 5 *
FROM dbo.vw_Sales_Product
ORDER BY sales_key DESC;
