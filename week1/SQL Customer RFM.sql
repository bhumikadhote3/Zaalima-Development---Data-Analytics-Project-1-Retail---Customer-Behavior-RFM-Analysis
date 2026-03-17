CREATE TABLE Customer_RFM (
    customer_key INT PRIMARY KEY,
    Recency INT,
    Frequency INT,
    Monetary FLOAT,
    R_score INT,
    F_score INT,
    M_score INT,
    Segment VARCHAR(50),
    Churn_Risk VARCHAR(20)
);

SELECT TOP 10 * FROM Customer_RFM;
