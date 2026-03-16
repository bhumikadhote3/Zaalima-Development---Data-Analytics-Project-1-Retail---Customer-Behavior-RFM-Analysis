USE RetailDB;
GO

IF OBJECT_ID('Dim_Customer','U') IS NULL
CREATE TABLE Dim_Customer (
    Customer_Key INT IDENTITY(1,1) PRIMARY KEY,
    LYLTY_CARD_NBR INT NOT NULL
);

IF OBJECT_ID('Dim_Product','U') IS NULL
CREATE TABLE Dim_Product (
    Product_Key INT IDENTITY(1,1) PRIMARY KEY,
    PROD_NBR INT NOT NULL,
    PROD_NAME VARCHAR(255),
    UNIT_PRICE DECIMAL(10,2)
);

IF OBJECT_ID('Dim_Date','U') IS NULL
CREATE TABLE Dim_Date (
    Date_Key INT PRIMARY KEY,
    Full_Date DATE NOT NULL,
    Day INT,
    Month INT,
    Month_Name VARCHAR(20),
    Quarter INT,
    Year INT
);

IF OBJECT_ID('Fact_Sales','U') IS NULL
CREATE TABLE Fact_Sales (
    Sales_Key INT IDENTITY(1,1) PRIMARY KEY,
    Date_Key INT,
    Customer_Key INT,
    Product_Key INT,
    Quantity INT,
    Revenue DECIMAL(12,2),

    FOREIGN KEY (Date_Key) REFERENCES Dim_Date(Date_Key),
    FOREIGN KEY (Customer_Key) REFERENCES Dim_Customer(Customer_Key),
    FOREIGN KEY (Product_Key) REFERENCES Dim_Product(Product_Key)
);
