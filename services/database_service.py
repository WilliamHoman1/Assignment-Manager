import sqlite3

DB_PATH = "data/assignments.db"


class DatabaseService:

    def get_problems(self):

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, topic, difficulty
            FROM problems
            ORDER BY position ASC
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows