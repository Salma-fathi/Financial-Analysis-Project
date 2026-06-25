import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('/home/ubuntu/finance.db')

# 1. Calculate RFM Metrics using SQL
# We'll use the latest date in the dataset as the reference point for Recency
rfm_query = """
WITH CustomerMetrics AS (
    SELECT 
        customer_id,
        MAX(full_date) AS last_transaction,
        COUNT(transaction_id) AS frequency,
        SUM(amount) AS monetary
    FROM Fact_Transactions f
    JOIN Dim_Time t ON f.time_id = t.time_id
    WHERE transaction_status = 'SUCCESS'
    GROUP BY customer_id
),
ReferenceDate AS (
    SELECT MAX(full_date) AS ref_date FROM Dim_Time
),
RFM_Raw AS (
    SELECT 
        m.customer_id,
        (JULIANDAY(r.ref_date) - JULIANDAY(m.last_transaction)) AS recency,
        m.frequency,
        m.monetary
    FROM CustomerMetrics m, ReferenceDate r
)
SELECT * FROM RFM_Raw;
"""

df_rfm = pd.read_sql_query(rfm_query, conn)

# 2. Assign Scores (1-5) based on quantiles
df_rfm['R_Score'] = pd.qcut(df_rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
df_rfm['F_Score'] = pd.qcut(df_rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
df_rfm['M_Score'] = pd.qcut(df_rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

# 3. Calculate RFM Score and Segment
df_rfm['RFM_Score'] = df_rfm['R_Score'].astype(str) + df_rfm['F_Score'].astype(str) + df_rfm['M_Score'].astype(str)

def segment_customer(row):
    score = int(row['R_Score']) + int(row['F_Score']) + int(row['M_Score'])
    if score >= 13: return 'Champions'
    elif score >= 10: return 'Loyal Customers'
    elif score >= 7: return 'Potential Loyalists'
    elif score >= 4: return 'At Risk'
    else: return 'Lost'

df_rfm['Segment'] = df_rfm.apply(segment_customer, axis=1)

# Save results back to database
df_rfm.to_sql('Customer_Segments', conn, if_exists='replace', index=False)

print("RFM Analysis completed and segments saved.")
print("\n--- Segment Distribution ---")
print(df_rfm['Segment'].value_counts())

conn.close()
