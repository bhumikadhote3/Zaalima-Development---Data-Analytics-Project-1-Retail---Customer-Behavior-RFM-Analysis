print("Script started...")

import pandas as pd
import datetime as dt

# Load Excel
df = pd.read_excel("RETAIL.xlsx")

print("Excel Loaded Successfully ✅")

# Convert DATE column to datetime
df['DATE'] = pd.to_datetime(df['DATE'])

# Set analysis date (1 day after last transaction)
analysis_date = df['DATE'].max() + dt.timedelta(days=1)

# Create RFM table
rfm = df.groupby('LYLTY_CARD_NBR').agg({
    'DATE': lambda x: (analysis_date - x.max()).days,  # Recency
    'TXN_ID': 'count',                                 # Frequency
    'TOT_SALES': 'sum'                                 # Monetary
})

# Rename columns
rfm.columns = ['Recency', 'Frequency', 'Monetary']

print("\nRFM Table Created ✅")
print(rfm.head())

# RFM Scoring (1-5 scale)

rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

print("\nRFM Scoring Done ✅")
print(rfm.head())

# Identify Champions (High R, F, M)
champions = rfm[(rfm['R_Score'] == 5) & 
                (rfm['F_Score'] == 5) & 
                (rfm['M_Score'] == 5)]

print("\nNumber of Champions Customers:", len(champions))
# RFM Scoring Done
print("\nRFM Scoring Done ✅")
print(rfm.head())


# =============================
# 🔥 ADD SEGMENTATION HERE
# =============================

def segment_customer(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4:
        return "Champions"
    elif row['F_Score'] >= 4:
        return "Loyal Customers"
    elif row['R_Score'] >= 4 and row['F_Score'] <= 2:
        return "New Customers"
    elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
        return "At Risk"
    elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
        return "Lost Customers"
    else:
        return "Regular Customers"

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

print("\nCustomer Segmentation Done ✅")
print(rfm['Segment'].value_counts())


# (Optional) Champions Count
champions = rfm[rfm['Segment'] == "Champions"]
print("\nNumber of Champions Customers:", len(champions))