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

    def add_problem(self, problem: dict):
        """Save a Claude-generated problem to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get the next available position
        cursor.execute("SELECT COALESCE(MAX(position), 0) + 1 FROM problems")
        next_position = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO problems (id, title, topic, difficulty, instructions, src_code, unit_tests, supplemental_files, use_test_files_package, position)
            VALUES (:id, :title, :topic, :difficulty, :instructions, :src_code, :unit_tests, :supplemental_files, :use_test_files_package, :position)
        """, {
            "id": problem["id"],
            "title": problem["title"],
            "topic": problem["topic"],
            "difficulty": problem["difficulty"],
            "instructions": problem["instructions"],
            "src_code": problem["src_code"],
            "unit_tests": problem["unit_tests"],
            "supplemental_files": problem.get("supplemental_files"),
            "use_test_files_package": problem.get("use_test_files_package", 0),
            "position": next_position
        })

        conn.commit()
        conn.close()

    def problem_exists(self, problem_id: str) -> bool:
        """Check if a problem ID already exists to avoid duplicates."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM problems WHERE id = ?", (problem_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def delete_problem(self, problem_id: str):
        """Permanently delete a problem from the database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM problems WHERE id = ?", (problem_id,))
            conn.commit()