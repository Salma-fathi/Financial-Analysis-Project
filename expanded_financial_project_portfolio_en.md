# Professional Case Study: Developing a Business Intelligence (BI) System for Financial Transaction Analysis and Fraud Detection

## 1. Project Summary

This initial financial transaction analysis project was expanded into a comprehensive case study, simulating real-world systems in financial institutions. The development involved six strategic steps, starting from data warehouse design and culminating in the integration of fraud prediction models, with a focus on extracting valuable business insights.

## 2. Six Development Steps

### Step 1: Data Warehouse Design (Star Schema)

The data was restructured from a single flat table into a professional **Star Schema** model. The model consists of:
*   **Fact Table (Fact_Transactions):** Contains core financial measurements.
*   **Dimension Tables:** Include `Dim_Customers` (customer data), `Dim_Channels` (payment channels), and `Dim_Time` (temporal details).
*   **Benefit:** Improved query performance and facilitated cross-dimensional analysis.

### Step 2: Customer Segmentation Analysis (RFM Analysis)

SQL was used to segment customers based on Recency, Frequency, and Monetary values. The results showed a strategic distribution of customers:
*   **Champions:** 194 customers.
*   **Loyal Customers:** 251 customers.
*   **At Risk:** 191 customers.
*   **Benefit:** Enabled the marketing team to target specific segments with tailored campaigns to maximize ROI.

### Step 3: Time-Series and Trend Analysis

Sales and fraud trends were analyzed over time. The analysis revealed fluctuations in monthly transaction volumes, with specific days showing a significant increase in fraud attempts.
*   **Benefit:** Predicting peak periods and optimizing the allocation of security and technical resources.

### Step 4: Dashboard Design

A wireframe for an interactive dashboard was designed, focusing on key performance indicators (KPIs) such as fraud rate by channel and country, and RFM segment distribution.
*   **Benefit:** Providing immediate and comprehensive insights for decision-makers.

### Step 5: Fraud Prediction (ML Integration)

A machine learning model (Random Forest) was integrated to predict the likelihood of fraud. The model identified **"amount"** and **"hour"** as the most significant factors influencing suspicious transactions.
*   **Benefit:** Transitioning from descriptive analysis (what happened?) to predictive analysis (what will happen?).

### Step 6: Telecom Sector Touches (Telecom Metrics)

Telecom-specific metrics such as **ARPU** (Average Revenue Per User) were integrated into the segmentation analysis, and digital payment channels (UPI/Netbanking) were linked to transaction growth rates.

## 3. Results and Business Insights

*   **Improved Security:** The Netbanking channel requires additional security measures due to its higher fraud rate.
*   **Growth Opportunities:** Focus on the "Champions" segment in Singapore and UAE to increase sales.
*   **Operational Efficiency:** Reduce transaction failure rates in specific channels to enhance customer experience.

## 4. Conclusion

This project demonstrates the ability to handle complex financial data and transform it into integrated business intelligence solutions that support organizational growth and protect assets.

## 5. SQL Queries Used

```sql
-- 1. Count total transactions
SELECT COUNT(*) AS total_transactions FROM Fact_Transactions;

-- 2. Distribution of transaction types
SELECT transaction_type, COUNT(*) AS count, SUM(amount) AS total_amount
FROM Fact_Transactions
GROUP BY transaction_type;

-- 3. Distribution of transaction status
SELECT transaction_status, COUNT(*) AS count
FROM Fact_Transactions
GROUP BY transaction_status;

-- 4. Top 5 countries by transaction volume
SELECT dc.country, COUNT(ft.transaction_id) AS count, SUM(ft.amount) AS total_amount
FROM Fact_Transactions ft
JOIN Dim_Customers dc ON ft.customer_id = dc.customer_id
GROUP BY dc.country
ORDER BY count DESC
LIMIT 5;

-- 5. Fraud rate analysis
SELECT fraud_flag, COUNT(*) AS count, (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Fact_Transactions)) AS percentage
FROM Fact_Transactions
GROUP BY fraud_flag;

-- 6. High-Value Transactions (Potential Anomalies) - Example, adjust threshold as needed
-- This query needs to be adapted for the new schema and potentially for a more robust anomaly detection
-- For simplicity, we'll use a direct amount threshold for demonstration
SELECT transaction_id, customer_id, amount
FROM Fact_Transactions
WHERE amount > (SELECT AVG(amount) * 3 FROM Fact_Transactions) -- Example threshold
ORDER BY amount DESC
LIMIT 10;

-- 7. Frequent Transactions by Same Customer (Potential Fraud) - Example, adjust threshold as needed
SELECT dc.customer_id, DATE(dt.full_date) AS t_date, COUNT(ft.transaction_id) AS daily_count, SUM(ft.amount) AS total_daily_amount
FROM Fact_Transactions ft
JOIN Dim_Customers dc ON ft.customer_id = dc.customer_id
JOIN Dim_Time dt ON ft.time_id = dt.time_id
GROUP BY dc.customer_id, t_date
HAVING daily_count > 5
ORDER BY daily_count DESC;

-- 8. Country-wise Fraud Percentage
SELECT dc.country, 
       COUNT(ft.transaction_id) AS total_tx, 
       SUM(ft.fraud_flag) AS fraud_tx,
       (SUM(ft.fraud_flag) * 100.0 / COUNT(ft.transaction_id)) AS fraud_rate
FROM Fact_Transactions ft
JOIN Dim_Customers dc ON ft.customer_id = dc.customer_id
GROUP BY dc.country
ORDER BY fraud_rate DESC;

-- 9. Channel-wise Risk Analysis
SELECT dch.channel_name AS channel, 
       COUNT(ft.transaction_id) AS total_tx, 
       SUM(ft.fraud_flag) AS fraud_tx,
       (SUM(ft.fraud_flag) * 100.0 / COUNT(ft.transaction_id)) AS fraud_rate
FROM Fact_Transactions ft
JOIN Dim_Channels dch ON ft.channel_id = dch.channel_id
GROUP BY dch.channel_name
ORDER BY fraud_rate DESC;
```
