# Financial Transaction Analysis and Fraud Detection Project

## Project Overview

This project is a comprehensive case study demonstrating advanced SQL skills, data warehousing concepts, and an introduction to machine learning for financial transaction analysis and fraud detection. It simulates a real-world Business Intelligence (BI) system for financial institutions, focusing on extracting valuable business insights from complex transactional data.

## Project Objectives

*   **Data Warehousing:** Design and implement a Star Schema for efficient data storage and retrieval.
*   **Customer Segmentation:** Perform RFM (Recency, Frequency, Monetary) analysis to segment customers based on their transactional behavior.
*   **Time-Series Analysis:** Analyze trends in transaction volume and fraud attempts over time.
*   **Dashboard Design:** Outline a professional dashboard structure for key performance indicators (KPIs).
*   **Fraud Prediction:** Integrate a machine learning model to identify potential fraudulent transactions.
*   **Business Insights:** Provide actionable insights for improving security, identifying growth opportunities, and enhancing operational efficiency.

## Methodology

The project was developed in six structured steps:

### Step 1: Data Warehouse Design (Star Schema)

*   **Description:** The raw transaction data was transformed and loaded into a Star Schema model. This involved creating a central `Fact_Transactions` table and several dimension tables: `Dim_Customers`, `Dim_Channels`, and `Dim_Time`.
*   **Tools:** SQLite, Python (Pandas for data loading).
*   **Files:** `step1_star_schema.py`

### Step 2: Customer Segmentation (RFM Analysis)

*   **Description:** Customers were segmented using RFM metrics calculated directly from the `Fact_Transactions` table. Segments included 'Champions', 'Loyal Customers', 'Potential Loyalists', 'At Risk', and 'Lost'.
*   **Tools:** SQL, Python (Pandas for scoring and segmentation logic).
*   **Files:** `step2_rfm_analysis.py`

### Step 3: Time-Series and Trend Analysis

*   **Description:** Monthly transaction volumes and daily fraud trends were analyzed to identify patterns and fluctuations over time.
*   **Tools:** SQL, Python (Matplotlib, Seaborn for visualization).
*   **Files:** `step3_time_series.py`
*   **Visualizations:**
    *   `monthly_trend.png`: Monthly Transaction Amount Trend
    *   `daily_fraud_trend.png`: Daily Fraud Transaction Trend

### Step 4: Dashboard Design

*   **Description:** A conceptual design for an interactive BI dashboard was created, outlining key KPIs, proposed charts (e.g., geographic heatmap, RFM segment breakdown), and interactive filters.
*   **Tools:** Markdown (conceptual design).
*   **Files:** `step4_dashboard_design.md`

### Step 5: Fraud Prediction (ML Integration)

*   **Description:** A Random Forest Classifier was trained to predict fraudulent transactions. Feature importance analysis identified `amount` and `hour` as key predictors.
*   **Tools:** Python (Scikit-learn, Pandas).
*   **Files:** `step5_ml_fraud.py`

### Step 6: Telecom Sector Touches & Final Documentation

*   **Description:** Incorporated telecom-specific metrics (e.g., ARPU in segmentation context) and finalized the project documentation, summarizing all findings and business insights.
*   **Tools:** Markdown.
*   **Files:** `expanded_financial_project_portfolio_en.md`

## Results and Business Insights

*   **Enhanced Security:** Identified `NETBANKING` channel and `USA` as areas requiring heightened fraud prevention measures.
*   **Targeted Marketing:** RFM analysis provides a basis for tailored marketing strategies to retain valuable customers and re-engage at-risk segments.
*   **Operational Efficiency:** Time-series analysis helps in resource allocation and proactive fraud detection during peak periods.

## How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone [YOUR_REPOSITORY_URL]
    cd [YOUR_REPOSITORY_NAME]
    ```
2.  **Set up the environment:**
    *   Ensure Python 3 and `pip` are installed.
    *   Install required Python libraries:
        ```bash
        pip install pandas scikit-learn matplotlib seaborn
        ```
3.  **Download the dataset:**
    *   The project uses `real_transactions.csv`. You can download it from [here](https://raw.githubusercontent.com/karanveer97/Financial-Transaction-Analysis/main/financial_transactions.csv) and place it in the project root directory.
4.  **Run the steps sequentially:**
    *   **Step 1 (Star Schema):** `python3 step1_star_schema.py`
    *   **Step 2 (RFM Analysis):** `python3 step2_rfm_analysis.py`
    *   **Step 3 (Time-Series Analysis):** `python3 step3_time_series.py`
    *   **Step 5 (ML Fraud Prediction):** `python3 step5_ml_fraud.py`

## Project Structure

```
. 
├── README.md
├── expanded_financial_project_portfolio_en.md
├── step1_star_schema.py
├── step2_rfm_analysis.py
├── step3_time_series.py
├── step4_dashboard_design.md
├── step5_ml_fraud.py
├── fraud_rate_by_country.png
├── monthly_trend.png
├── daily_fraud_trend.png
├── fraud_risk_by_channel.png
├── finance.db (generated after running step1_star_schema.py)
└── real_transactions.csv (downloaded dataset)
```

## Author

Salma Mohammed

## License

This project is open-sourced under the MIT License. See the LICENSE file for details.
