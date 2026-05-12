import os
from dotenv import load_dotenv
import pymysql
from datetime import datetime, timedelta

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    charset="utf8mb4"
)
cursor = conn.cursor()
now = datetime.now()

cursor.executemany(
    "INSERT IGNORE INTO customers (customer_id, name, email) VALUES (%s, %s, %s)",
    [
        (1, "Alice Chen", "alice@example.com"),
        (2, "Bob Wang",   "bob@example.com"),
    ]
)

cursor.executemany(
    "INSERT IGNORE INTO orders (order_id, customer_id, product_name, status, order_date, delivery_date) VALUES (%s,%s,%s,%s,%s,%s)",
    [
        (1001,  1, "Wireless Headphones", "delivered",  now - timedelta(days=10), now - timedelta(days=3)),
        (5678,  1, "Mechanical Keyboard", "delivered",  now - timedelta(days=5),  now - timedelta(days=1)),
        (7890,  2, "USB-C Hub",           "delivered",  now - timedelta(days=2),  now - timedelta(days=1)),
        (2222,  2, "Laptop Stand",        "shipped",    now - timedelta(days=1),  None),
        (12345, 1, "Monitor Arm",         "processing", now,                      None),
    ]
)

cursor.executemany(
    "INSERT IGNORE INTO customer_memory (customer_id, key_name, value) VALUES (%s, %s, %s)",
    [
        (1, "past_issue",  "Order 1001 was delivered 2 days late"),
        (1, "past_issue",  "Order 5678 had wrong item delivered"),
        (1, "preference",  "prefers_refund_over_exchange"),
    ]
)

conn.commit()
cursor.close()
conn.close()
print("測試資料填入完成")
