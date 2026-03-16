# ==========================================
# Member 1: Data Extraction from CSV (Spyder Ready)
# Week 2 – Logic Core (Python)
# ==========================================

import pandas as pd
import os

# -------------------------------
# 1. File Path (Change if needed)
# -------------------------------
csv_path = r"C:\Users\my\Desktop\Zaalima 2month internship\p1\RETAIL.csv"

# Optional: check if file exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at {csv_path}")

# -------------------------------
# 2. Load CSV into pandas
# -------------------------------
df_retail = pd.read_csv(csv_path)

print("✅ CSV loaded successfully!")
print(f"Total rows in original CSV: {len(df_retail)}")

# -------------------------------
# 3. Preview Data
# -------------------------------
print("\nFirst 5 rows:")
print(df_retail.head())

print("\nColumns:")
print(df_retail.columns)

# -------------------------------
# 4. Basic Validation
# -------------------------------
print("\n--- Null Value Check ---")
print(df_retail.isnull().sum())

print("\n--- Summary Statistics ---")
print(df_retail.describe())

# -------------------------------
# 5. Create Cleaned DataFrame
# -------------------------------
df_cleaned = df_retail[
    (df_retail['LYLTY_CARD_NBR'].notnull()) &
    (df_retail['PROD_QTY'] > 0) &
    (df_retail['UNIT_PRICE'] > 0) &
    (df_retail['TOT_SALES'] > 0)
].copy()

# Add revenue column
df_cleaned['revenue'] = df_cleaned['PROD_QTY'] * df_cleaned['UNIT_PRICE']

print("\n✅ Cleaned DataFrame ready!")
print(f"Total rows after cleaning: {len(df_cleaned)}")

# Preview cleaned data
print(df_cleaned.head())

# -------------------------------
# 6. Optional: Save Cleaned CSV for next member
# -------------------------------
cleaned_csv_path = r"C:\Users\my\Desktop\Zaalima 2month internship\p1\Retail_Cleaned.csv"
df_cleaned.to_csv(cleaned_csv_path, index=False)
print(f"\n✅ Cleaned data saved to {cleaned_csv_path}")

# -------------------------------
# 7. End of Member 1 Script
# -------------------------------
print("\n🎯 Member 1 Completed: Data Extraction & Cleaning")


# ==========================================
# Member 2: RFM Calculation
# Spyder / Python 3.x
# ==========================================

import pandas as pd
from datetime import datetime

# -------------------------------
# 1. Load Cleaned Data
# -------------------------------
cleaned_csv_path = r"C:\Users\my\Desktop\Zaalima 2month internship\p1\Retail_Cleaned.csv"
df = pd.read_csv(cleaned_csv_path)

print("✅ Cleaned CSV loaded!")
print(f"Total rows: {len(df)}")
print(df.head())

# -------------------------------
# 2. Convert DATE column to datetime
# -------------------------------
df['DATE'] = pd.to_datetime(df['DATE'], dayfirst=True)  # your DATE is DD-MM-YYYY
print("\n✅ DATE column converted to datetime.")

# -------------------------------
# 3. Set reference date for Recency
# -------------------------------
# Recency is calculated as days since last purchase
# We'll take reference date as the day after the last order date
reference_date = df['DATE'].max() + pd.Timedelta(days=1)
print(f"\nReference date for Recency: {reference_date.date()}")

# -------------------------------
# 4. Calculate RFM metrics
# -------------------------------
rfm = df.groupby('LYLTY_CARD_NBR').agg({
    'DATE': lambda x: (reference_date - x.max()).days,  # Recency
    'TXN_ID': 'count',                                   # Frequency
    'revenue': 'sum'                                     # Monetary
}).reset_index()

# Rename columns
rfm.rename(columns={
    'DATE': 'Recency',
    'TXN_ID': 'Frequency',
    'revenue': 'Monetary'
}, inplace=True)

print("\n✅ RFM metrics calculated.")
print(rfm.head())

# -------------------------------
# 5. Save RFM table to CSV
# -------------------------------
rfm_csv_path = r"C:\Users\my\Desktop\Zaalima 2month internship\p1\RFM_Table.csv"
rfm.to_csv(rfm_csv_path, index=False)
print(f"\n✅ RFM table saved to {rfm_csv_path}")

# -------------------------------
# 6. End of Member 2
# -------------------------------
print("\n🎯 Member 2 Completed: RFM Calculation")


# ==========================================
# Member 3: RFM Scoring & Customer Segmentation
# Spyder / Python 3.x
# ==========================================

import pandas as pd

# -------------------------------
# 1. Load RFM Table from Member 2
# -------------------------------
rfm_csv_path = r"C:\Users\my\Desktop\Zaalima 2month internship\p1\RFM_Table.csv"
rfm = pd.read_csv(rfm_csv_path)

print("✅ RFM Table loaded!")
print(f"Total customers: {len(rfm)}")
print(rfm.head())

# -------------------------------
# 2. Calculate R, F, M scores (1-5 scale)
# -------------------------------
# Recency: lower is better → score 5 for most recent
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]).astype(int)

# Frequency: higher is better → score 5 for highest frequency
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)

# Monetary: higher is better → score 5 for highest spending
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5]).astype(int)

# -------------------------------
# 3. Combine RFM score
# -------------------------------
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

print("\n✅ RFM Scores calculated:")
print(rfm.head())

# -------------------------------
# 4. Customer Segmentation
# -------------------------------
def segment_customer(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Champion'
    elif row['R_Score'] >= 3 and row['F_Score'] >= 3 and row['M_Score'] >= 3:
        return 'Loyal'
    elif row['R_Score'] >= 3 and row['F_Score'] <= 2:
        return 'At Risk'
    elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
        return 'Lost'
    else:
        return 'Need Attention'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

print("\n✅ Customer Segmentation done:")
print(rfm[['LYLTY_CARD_NBR','RFM_Score','Segment']].head())

# -------------------------------
# 5. Save Final RFM + Segment Table
# -------------------------------
final_csv_path = r"C:\Users\my\Desktop\Zaalima 2month internship\p1\RFM_Segmented.csv"
rfm.to_csv(final_csv_path, index=False)
print(f"\n✅ Final RFM + Segment table saved to {final_csv_path}")

# -------------------------------
# 6. End of Member 3
# -------------------------------
print("\n🎯 Member 3 Completed: RFM Scoring & Customer Segmentation")


# ==========================================
# Member 4: RFM Segment Visualization
# Spyder / Python 3.x
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# 1. Load segmented RFM table
# -------------------------------
rfm_segmented_path = r"C:\Users\my\Desktop\Zaalima 2month internship\p1\RFM_Segmented.csv"
rfm = pd.read_csv(rfm_segmented_path)

print("✅ RFM Segmented table loaded!")
print(rfm.head())

# -------------------------------
# 2. Count of customers by Segment
# -------------------------------
segment_counts = rfm['Segment'].value_counts()
print("\nCustomer counts by segment:")
print(segment_counts)

# -------------------------------
# 3. Plot Segment Distribution
# -------------------------------
plt.figure(figsize=(8,5))
sns.barplot(x=segment_counts.index, y=segment_counts.values, palette="Set2")
plt.title("Customer Count by RFM Segment")
plt.ylabel("Number of Customers")
plt.xlabel("Segment")
plt.xticks(rotation=30)
plt.show()

# -------------------------------
# 4. Optional: Scatter plot of Recency vs Monetary colored by Segment
# -------------------------------
plt.figure(figsize=(8,5))
sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Segment', palette="Set1", s=100)
plt.title("Recency vs Monetary by Segment")
plt.xlabel("Recency (days)")
plt.ylabel("Monetary ($)")
plt.show()

# -------------------------------
# 5. Optional: Scatter plot of Frequency vs Monetary colored by Segment
# -------------------------------
plt.figure(figsize=(8,5))
sns.scatterplot(data=rfm, x='Frequency', y='Monetary', hue='Segment', palette="Set1", s=100)
plt.title("Frequency vs Monetary by Segment")
plt.xlabel("Frequency (Number of Purchases)")
plt.ylabel("Monetary ($)")
plt.show()

print("\n🎯 Member 4 Completed: RFM Visualization")