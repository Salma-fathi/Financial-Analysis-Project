import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('/home/ubuntu/finance.db')
cursor = conn.cursor()

# 1. Create Dimension Tables
cursor.executescript("""
-- Dim_Customers
CREATE TABLE IF NOT EXISTS Dim_Customers (
    customer_id INTEGER PRIMARY KEY,
    country TEXT
);

-- Dim_Channels
CREATE TABLE IF NOT EXISTS Dim_Channels (
    channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_name TEXT UNIQUE
);

-- Dim_Time
CREATE TABLE IF NOT EXISTS Dim_Time (
    time_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date TEXT,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER
);

-- Fact_Transactions
CREATE TABLE IF NOT EXISTS Fact_Transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    channel_id INTEGER,
    time_id INTEGER,
    transaction_type TEXT,
    amount REAL,
    transaction_status TEXT,
    fraud_flag INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Dim_Customers(customer_id),
    FOREIGN KEY (channel_id) REFERENCES Dim_Channels(channel_id),
    FOREIGN KEY (time_id) REFERENCES Dim_Time(time_id)
);
""")

# 2. Populate Dimension Tables
# Dim_Customers
cursor.execute("INSERT OR IGNORE INTO Dim_Customers (customer_id, country) SELECT DISTINCT customer_id, country FROM transactions")

# Dim_Channels
cursor.execute("INSERT OR IGNORE INTO Dim_Channels (channel_name) SELECT DISTINCT channel FROM transactions")

# Dim_Time (Parsing transaction_date)
df_time = pd.read_sql_query("SELECT DISTINCT transaction_date FROM transactions", conn)
df_time['transaction_date'] = pd.to_datetime(df_time['transaction_date'])
df_time['year'] = df_time['transaction_date'].dt.year
df_time['month'] = df_time['transaction_date'].dt.month
df_time['day'] = df_time['transaction_date'].dt.day
df_time['hour'] = df_time['transaction_date'].dt.hour
df_time['full_date'] = df_time['transaction_date'].dt.strftime('%Y-%m-%d %H:%M:%S')

for _, row in df_time.iterrows():
    cursor.execute("INSERT INTO Dim_Time (full_date, year, month, day, hour) VALUES (?, ?, ?, ?, ?)", 
                   (row['full_date'], row['year'], row['month'], row['day'], row['hour']))

# 3. Populate Fact Table
cursor.execute("""
INSERT INTO Fact_Transactions (transaction_id, customer_id, channel_id, time_id, transaction_type, amount, transaction_status, fraud_flag)
SELECT 
    t.transaction_id, 
    t.customer_id, 
    c.channel_id, 
    dt.time_id, 
    t.transaction_type, 
    t.amount, 
    t.transaction_status, 
    t.fraud_flag
FROM transactions t
JOIN Dim_Channels c ON t.channel = c.channel_name
JOIN Dim_Time dt ON t.transaction_date = dt.full_date
""")

conn.commit()
print("Star Schema implemented and data migrated successfully.")

# Verify the structure
print("\n--- Fact_Transactions Preview ---")
print(pd.read_sql_query("SELECT * FROM Fact_Transactions LIMIT 5", conn))

conn.close()
