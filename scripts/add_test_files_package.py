"""Script used to add test files column into database after database was created"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "assignments.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    ALTER TABLE problems
    ADD COLUMN use_test_files_package INTEGER DEFAULT 0
""")

conn.commit()
conn.close()

print("Column added successfully.")