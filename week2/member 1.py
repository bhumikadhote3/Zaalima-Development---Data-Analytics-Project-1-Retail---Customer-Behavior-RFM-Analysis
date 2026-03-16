import pyodbc
import pandas as pd

print("Member 1: Data Extraction Started...")

# Connect to SQL Server
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-V1J58F5\\SQLEXPRESS;"
    "DATABASE=RetailDW;"
    "Trusted_Connection=yes;"
)

# Pull data
query = "SELECT * FROM Fact_Sales"
df = pd.read_sql(query, conn)

print("Data Pulled Successfully ✅")

# Validation
print("Total Rows:", len(df))
print("Null Values:\n", df.isnull().sum())

conn.close()