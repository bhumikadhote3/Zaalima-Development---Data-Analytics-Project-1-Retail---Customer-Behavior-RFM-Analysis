# ============================================
# RFM AUTOMATION SCRIPT - FINAL STABLE VERSION
# ============================================

import pyodbc
import pandas as pd
import sys
from datetime import datetime

print("===================================")
print("Starting RFM Automation Process...")
print("===================================")

# --------------------------------------------
# STEP 1: SQL CONNECTION
# --------------------------------------------

try:
    print("Connecting to SQL Server...")

    conn = pyodbc.connect(
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=DESKTOP-V1J58F5\SQLEXPRESS;"
        r"DATABASE=RetailDB;"
        r"Trusted_Connection=yes;"
    )

    print("Connection Successful ✅")

except Exception as e:
    print("Connection Failed ❌")
    print(e)
    sys.exit()

# --------------------------------------------
# STEP 2: LOAD DATA (FROM VIEW)
# --------------------------------------------

try:
    print("Pulling data from dbo.vw_Sales_Product...")

    query = """
    SELECT 
        sales_key,
        customer_key,
        product_name,
        order_date,
        quantity,
        revenue
    FROM dbo.vw_Sales_Product
    """

    df = pd.read_sql(query, conn)

    print("Data Loaded Successfully ✅")
    print("Total Rows:", df.shape[0])

except Exception as e:
    print("Error while loading data ❌")
    print(e)
    sys.exit()

# --------------------------------------------
# STEP 3: DATA CLEANING
# --------------------------------------------

print("Cleaning data...")

df.dropna(inplace=True)
df['order_date'] = pd.to_datetime(df['order_date'])

print("Data Cleaning Completed ✅")

# --------------------------------------------
# STEP 4: RFM CALCULATION
# --------------------------------------------

print("Calculating RFM...")

today = df['order_date'].max()

rfm = df.groupby('customer_key').agg({
    'order_date': lambda x: (today - x.max()).days,
    'sales_key': 'count',
    'revenue': 'sum'
}).reset_index()

rfm.columns = ['customer_key', 'Recency', 'Frequency', 'Monetary']

print("RFM Calculation Completed ✅")
print("Total Customers:", rfm.shape[0])

# --------------------------------------------
# STEP 5: SAFE RFM SCORING
# --------------------------------------------

print("Applying RFM Scoring...")

def safe_qcut(series, labels):
    try:
        return pd.qcut(series, q=5, labels=labels, duplicates='drop')
    except:
        return pd.cut(series, bins=5, labels=labels)

rfm['R_score'] = safe_qcut(rfm['Recency'], [5,4,3,2,1])
rfm['F_score'] = safe_qcut(rfm['Frequency'], [1,2,3,4,5])
rfm['M_score'] = safe_qcut(rfm['Monetary'], [1,2,3,4,5])

rfm[['R_score','F_score','M_score']] = (
    rfm[['R_score','F_score','M_score']]
    .astype(float)
    .fillna(3)
)

rfm['RFM_Score'] = (
    rfm['R_score'].astype(int).astype(str) +
    rfm['F_score'].astype(int).astype(str) +
    rfm['M_score'].astype(int).astype(str)
)

print("Scoring Completed ✅")

# --------------------------------------------
# STEP 6: PROFESSIONAL SEGMENTATION (UPDATED)
# --------------------------------------------

print("Creating Customer Segments...")

def segment(row):
    if row['R_score'] >= 4 and row['F_score'] >= 4:
        return "Champions"
    elif row['R_score'] >= 3 and row['F_score'] >= 3:
        return "Loyal Customers"
    elif row['R_score'] <= 2 and row['F_score'] <= 2:
        return "Hibernating"
    elif row['R_score'] <= 2:
        return "At Risk"
    else:
        return "Potential Loyalists"

rfm['Segment'] = rfm.apply(segment, axis=1)

print("Segmentation Completed ✅")

# --------------------------------------------
# STEP 7: ADD CHURN RISK COLUMN (NEW)
# --------------------------------------------

print("Adding Churn Risk Column...")

def churn_flag(row):
    if row['Recency'] > 90 and row['Frequency'] <= 2:
        return "High Risk"
    elif 60 < row['Recency'] <= 90:
        return "Medium Risk"
    else:
        return "Low Risk"

rfm['Churn_Risk'] = rfm.apply(churn_flag, axis=1)

print("Churn Risk Column Added ✅")

# --------------------------------------------
# STEP 8: EXPORT
# --------------------------------------------

print("Exporting results to CSV...")

rfm.to_csv("rfm_output.csv", index=False)

print("Export Completed ✅")
print("Saving RFM results to SQL table...")

cursor = conn.cursor()

# Step 1: Delete old data
cursor.execute("DELETE FROM Customer_RFM")
conn.commit()

# Step 2: Insert new RFM data
for index, row in rfm.iterrows():
    cursor.execute("""
        INSERT INTO Customer_RFM
        (customer_key, Recency, Frequency, Monetary,
         R_score, F_score, M_score, Segment, Churn_Risk)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        int(row['customer_key']),
        int(row['Recency']),
        int(row['Frequency']),
        float(row['Monetary']),
        int(row['R_score']),
        int(row['F_score']),
        int(row['M_score']),
        row['Segment'],
        row['Churn_Risk']
    )

conn.commit()
print("RFM data saved to SQL successfully ✅")
print("File saved as: rfm_output.csv")

# --------------------------------------------
# FINISH
# --------------------------------------------

conn.close()

print("===================================")
print("RFM Automation Completed Successfully 🚀")
print("===================================")

# --------------------------------------------
# STEP 9: MARKET BASKET ANALYSIS
# --------------------------------------------

print("Running Market Basket Analysis...")

basket = df.groupby(['sales_key', 'product_name'])['quantity'] \
           .sum().unstack().fillna(0)

basket = (basket > 0)

from mlxtend.frequent_patterns import apriori, association_rules

frequent_items = apriori(basket, min_support=0.005, use_colnames=True)
rules = association_rules(frequent_items, metric="lift", min_threshold=1)

print("Top Rules:")
print(rules.head())

print(df.groupby('sales_key')['product_name'].nunique().value_counts())