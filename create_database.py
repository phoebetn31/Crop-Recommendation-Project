import sqlite3
import os

# tạo thư mục nếu chưa có
os.makedirs("database", exist_ok=True)

# kết nối database
conn = sqlite3.connect("database/crop_prediction.db")

cursor = conn.cursor()

# tạo bảng
cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    N REAL,
    P REAL,
    K REAL,
    temperature REAL,
    humidity REAL,
    ph REAL,
    rainfall REAL,
    prediction TEXT,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database created successfully!")