import pandas as pd
import datetime as dt

print("Member 2: RFM Calculation Started...")

df = pd.read_excel("RETAIL.xlsx")

df['DATE'] = pd.to_datetime(df['DATE'])

analysis_date = df['DATE'].max() + dt.timedelta(days=1)

rfm = df.groupby('LYLTY_CARD_NBR').agg({
    'DATE': lambda x: (analysis_date - x.max()).days,
    'TXN_ID': 'count',
    'TOT_SALES': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

print("RFM Table Created ✅")
print(rfm.head())