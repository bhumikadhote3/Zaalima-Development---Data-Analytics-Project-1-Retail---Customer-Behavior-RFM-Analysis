# Zaalima-Development---Data-Analytics-Project-1-Retail---Customer-Behavior-RFM-Analysis
Retail Customer Behavior &amp; RFM Analysis project using SQL Server, Python, and Power BI. It cleans retail transaction data, builds a star schema warehouse, performs RFM customer segmentation, and generates insights on high-value and churn-risk customers through an automated analytics pipeline and dashboard.

# Retail Customer Behavior & RFM Analysis
#Project Overview

This project analyzes retail transaction data to understand customer purchasing behavior using the RFM (Recency, Frequency, Monetary) model. The system identifies high-value customers, loyal customers, and churn-risk customers to support targeted marketing and customer retention strategies.

The project simulates a real-world enterprise analytics pipeline covering data engineering, analytics processing, visualization, and automation.

# Tech Stack

1.SQL Server — Data cleaning and warehouse design

2.Python (Pandas, NumPy) — Data processing and RFM analysis

3.Power BI — Interactive business dashboard

Git & GitHub — Version control and project management

#Project Architecture

Raw Retail Data → SQL Data Cleaning → Star Schema Data Warehouse → Python RFM Engine → Segmentation Output → Power BI Dashboard → Automated Pipeline

# Project Structure
Retail-Customer-RFM-Analysis
│
├── week1
│   ├── Schema_SQL.sql
│   ├── SQL data cleaning.sql
│   ├── retail analysis SQL.sql
│   ├── vw_Sales_Product.sql
│
├── week2
│   ├── rfm_automation.py
│   ├── member1_data_extract.py
│   ├── member2.py
│   ├── mba_demo.py
│
├── week3
│   └── visualization.pbix
│
├── week4
│   ├── run_rfm.bat
│   └── data_pipeline_validation.sql
│
├── data
│   └── RETAIL.csv
│
└── output
    ├── RFM_Table.csv
    ├── RFM_Segmented.csv
    └── rfm_output.csv

# Key Features

Retail transaction data cleaning using SQL

Star schema data warehouse design

RFM customer segmentation model

Market Basket Analysis for product association

Interactive Power BI dashboard

Automated analytics pipeline

# Business Insights

Identify high-value customers (Champions)

Detect churn-risk customers

Analyze product purchasing patterns

Support data-driven marketing strategies
