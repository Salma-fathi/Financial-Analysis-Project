import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Connect to the database
conn = sqlite3.connect('/home/ubuntu/finance.db')

# 1. Prepare Features and Target using SQL
query_ml = """
SELECT 
    f.amount, 
    f.fraud_flag,
    c.country,
    ch.channel_name,
    t.hour,
    t.month
FROM Fact_Transactions f
JOIN Dim_Customers c ON f.customer_id = c.customer_id
JOIN Dim_Channels ch ON f.channel_id = ch.channel_id
JOIN Dim_Time t ON f.time_id = t.time_id;
"""
df_ml = pd.read_sql_query(query_ml, conn)

# 2. Preprocessing (One-hot encoding for categorical variables)
df_ml = pd.get_dummies(df_ml, columns=['country', 'channel_name'])

X = df_ml.drop('fraud_flag', axis=1)
y = df_ml['fraud_flag']

# 3. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train a simple Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluation
y_pred = model.predict(X_test)
print("\n--- Model Evaluation ---")
print(classification_report(y_test, y_pred))

# 6. Feature Importance
feature_importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\n--- Top Features for Fraud Prediction ---")
print(feature_importance.head(5))

conn.close()
