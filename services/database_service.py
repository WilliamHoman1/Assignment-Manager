import sqlite3

DB_PATH = "data/assignments.db"


class DatabaseService:

    def __init__(self):
        self.db_path = DB_PATH

    def get_problems(self):
        """Return list of problems for the problems table"""

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, topic, difficulty
            FROM problems
            ORDER BY position
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_problem(self, problem_id):
        """Return full problem details for preview"""

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, instructions, src_code, unit_tests
            FROM problems
            WHERE id = ?
        """, (problem_id,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return dict(row)