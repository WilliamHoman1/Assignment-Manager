import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "assignments.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    ALTER TABLE problems
    ADD COLUMN supplemental_files TEXT
""")

conn.commit()
conn.close()

print("Column added successfully.")