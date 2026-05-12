import os
from dotenv import load_dotenv
import pymysql

load_dotenv() #讀取目錄下的env

# 用來跟資料庫連線用的資訊
conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    charset="utf8mb4"
)
cursor = conn.cursor()#在python中執行SQL指令用

statements = [ # 建立四個table 客戶資訊、訂單、投訴表、長期記憶
    """CREATE TABLE IF NOT EXISTS customers (
        customer_id INT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY,
        customer_id INT,
        product_name TEXT,
        status VARCHAR(50),
        order_date TIMESTAMP,
        delivery_date TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS complaints (
        complaint_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        order_id INT,
        issue TEXT,
        status VARCHAR(50) DEFAULT 'open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS customer_memory (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        key_name VARCHAR(100),
        value TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""
]

for stmt in statements: # 向mysql發送指令
    cursor.execute(stmt)

conn.commit()# 正式提交
cursor.close()
conn.close()# 關閉資源
print("Table 建立完成")
