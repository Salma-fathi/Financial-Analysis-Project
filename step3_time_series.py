import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the database
conn = sqlite3.connect('/home/ubuntu/finance.db')

# 1. Monthly Transaction Volume and Amount
query_monthly = """
SELECT 
    t.year, 
    t.month, 
    COUNT(f.transaction_id) AS total_count, 
    SUM(f.amount) AS total_amount
FROM Fact_Transactions f
JOIN Dim_Time t ON f.time_id = t.time_id
GROUP BY t.year, t.month
ORDER BY t.year, t.month;
"""
df_monthly = pd.read_sql_query(query_monthly, conn)
df_monthly['period'] = df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str).str.zfill(2)

# 2. Daily Fraud Trend
query_daily_fraud = """
SELECT 
    DATE(t.full_date) AS date, 
    SUM(f.fraud_flag) AS fraud_count
FROM Fact_Transactions f
JOIN Dim_Time t ON f.time_id = t.time_id
GROUP BY date
ORDER BY date;
"""
df_daily_fraud = pd.read_sql_query(query_daily_fraud, conn)

# Visualizations
plt.figure(figsize=(12, 6))
sns.lineplot(x='period', y='total_amount', data=df_monthly, marker='o', label='Total Amount')
plt.title('Monthly Transaction Amount Trend', fontsize=15)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/home/ubuntu/monthly_trend.png')
plt.close()

plt.figure(figsize=(12, 6))
sns.lineplot(x='date', y='fraud_count', data=df_daily_fraud, color='red', label='Fraud Count')
plt.title('Daily Fraud Transaction Trend', fontsize=15)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/home/ubuntu/daily_fraud_trend.png')
plt.close()

print("Time-Series Analysis completed and visualizations saved.")
conn.close()
