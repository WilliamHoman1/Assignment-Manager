import sqlite3
import gitlab
import os


class AssignmentService:

    def __init__(self, db_name="data/assignments.db"):

        self.db_name = db_name
        self.token = os.getenv("GITLAB_TOKEN")

        if not self.token:
            raise Exception("GITLAB_TOKEN not set")

        self.gl = gitlab.Gitlab("https://gitlab.com", private_token=self.token)

    def create_assignment(self, assignment_id, title, problem_ids):
        """Create assignment repo and export problems"""

        # 1. create GitLab project (repo)
        project = self.gl.projects.create({
            'name': assignment_id,
            'visibility': 'private'
        })

        # 2. build local export structure
        export_dir = f"exports/{assignment_id}"
        os.makedirs(export_dir, exist_ok=True)

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        for pid in problem_ids:
            cursor.execute("""
                SELECT instructions, unit_tests
                FROM problems
                WHERE id = ?
            """, (pid,))

            row = cursor.fetchone()
            if not row:
                continue

            instructions, tests = row

            problem_dir = os.path.join(export_dir, pid)
            os.makedirs(problem_dir, exist_ok=True)

            with open(os.path.join(problem_dir, "instructions.md"), "w") as f:
                f.write(instructions or "")

            with open(os.path.join(problem_dir, "tests.py"), "w") as f:
                f.write(tests or "")

        conn.close()

        # 3. commit export to GitLab repo
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, export_dir)

                with open(file_path, "r") as f:
                    content = f.read()

                project.files.create({
                    'file_path': rel_path,
                    'branch': 'main',
                    'content': content,
                    'commit_message': f'Add {rel_path}'
                })

        return project.web_url

    def get_assignment_problems(self, assignment_id):
        """Return problems for display (optional)"""

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.id, p.title, p.instructions, p.unit_tests
            FROM problems p
            JOIN assignment_problems ap ON p.id = ap.problem_id
            WHERE ap.assignment_id = ?
        """, (assignment_id,))

        rows = cursor.fetchall()
        conn.close()

        return rows