import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "assignments.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE problems ADD COLUMN src_code TEXT;")
    print("src_code column added.")
except sqlite3.OperationalError as e:
    print(f"OperationalError: {e}")

conn.commit()
conn.close()