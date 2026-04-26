

import sqlite3
import os
from dotenv import load_dotenv
import gitlab

# Load environment variables from .env
load_dotenv()


class AssignmentService:
    """Service that creates the assignment in GitLab. Transfers what is chosen by
    user and moves it to its own repository for students to clone."""

    def __init__(self, db_name="data/assignments.db"):
        self.db_name = db_name
        self.token = os.getenv("GITLAB_TOKEN")
        if not self.token:
            raise Exception("GITLAB_TOKEN not set")
        self.gl = gitlab.Gitlab("https://gitlab.com", private_token=self.token)

    def create_assignment(self, assignment_id, title, problem_ids, problem_set_number):
        """
        Create GitLab repo and export problems with src, tests, instructions,
        including default root README.md for the assignment.
        """
        # 1. Create GitLab project
        try:
            project = self.gl.projects.create({
                "name": assignment_id,
                "visibility": "private"
            })
        except gitlab.exceptions.GitlabCreateError:
            raise Exception(f"Assignment name '{assignment_id}' is already used in GitLab. Please choose a different problem set number.")

        # 2. Create local folder structure
        export_dir = os.path.join("exports", assignment_id)
        os.makedirs(export_dir, exist_ok=True)

        # 3. Fetch problems from DB
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        for pid in problem_ids:
            cursor.execute("""
                SELECT instructions, unit_tests, src_code
                FROM problems
                WHERE id = ?
            """, (pid,))
            row = cursor.fetchone()
            if not row:
                print(f"Problem {pid} not found in database, skipping.")
                continue

            instructions, tests, src_code = row

            # 4. Create flat folder for this problem
            problem_dir = os.path.join(export_dir, pid)
            os.makedirs(problem_dir, exist_ok=True)

            # 5. Write problem README
            readme_path = os.path.join(problem_dir, "README.md")
            with open(readme_path, "w") as f:
                f.write(instructions or "")

            # 6. Write source code — named simply so tests can import it
            src_file_path = os.path.join(problem_dir, f"{pid}.py")
            with open(src_file_path, "w") as f:
                f.write(src_code or "")

            # 7. Write unit tests — in same folder as src so import works
            test_file_path = os.path.join(problem_dir, f"test_{pid}.py")
            with open(test_file_path, "w") as f:
                # Fix the import line to match the actual filename
                fixed_tests = self._fix_import(tests or "", pid)
                f.write(fixed_tests)

        conn.close()

        # 8. Write root README
        root_readme_path = os.path.join(export_dir, "README.md")
        with open(root_readme_path, "w") as f:
            f.write(self.default_root_readme(problem_set_number))

        # 9. Push files to GitLab
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, export_dir)
                with open(file_path, "r") as f:
                    content = f.read()
                try:
                    project.files.create({
                        "file_path": rel_path,
                        "branch": "main",
                        "content": content,
                        "commit_message": f"Add {rel_path}"
                    })
                except gitlab.exceptions.GitlabCreateError as e:
                    print(f"Warning: Could not add {rel_path} to GitLab: {e}")

        return project.web_url

    def _fix_import(self, test_code: str, problem_id: str) -> str:
        """
        Replace any 'import problem_one' style imports with
        the actual problem file name so tests can find the source file.
        """
        import re
        # Replace any 'import problem_xxx' with 'import <problem_id>'
        fixed = re.sub(r'import problem_\w+', f'import {problem_id}', test_code)
        # Also replace 'problem_xxx.function' calls with '<problem_id>.function'
        fixed = re.sub(r'problem_\w+\.', f'{problem_id}.', fixed)
        return fixed

    @staticmethod
    def default_root_readme(problem_set_number: int) -> str:
        """
        Returns the default README content for a new assignment.
        Includes introduction, point breakdown, and policy reminders.
        """
        return f"""# Problem Set Lab {problem_set_number} - 35pts
*Programming Practice*

**See the grading schedule linked in D2L for the deadline extension details**

## Introduction
This is your Problem Set Lab assignment. In this assignment, you will be presented with a set 
of problems. Each problem indicates the total amount of points, broken down into specific requirements. 
For each problem, it will indicate the corresponding file to update under **Provided File**.

Points are described as either:
1. **Point Breakdown:** Completing the tasks awards the described points.
2. **Point Categories:** You earn the points depending on the category that best described your answer.

## Information on attributes
- [Unit Test(s) Provided] - There are test files available for you to run against your solution.
- [AI - Research Only] - You may use AI for research purposes only. This includes asking it about the general topic
the question addresses, providing examples of those topics with explanations, and offering additional resources you
can use to learn more. You may not use AI to solve the problem and copy/paste the solution it provides. The solution
should be written by yourself.
- [Extended Description Req.] - Part of this problem requires that you use the extended description of a commit to
provide an answer.


## Fast, Automated Feedback Through Unit Tests

As you work on your program, many problems will include unit tests. These programs run your code and compare it to 
expected solutions and output. Unit tests provide **automated feedback** but do not represent the final grade.

## On Comments and Documentation

Throughout this course, part of the grade for these problems will be how well you document your code. For this assignment,
we will focus on regular inline comments that start with a pound or hashtag sign (#).

## Policy Reminder - AI

For lab assignments, AI use is specified per problem. You are allowed to use AI for this assignment in the context of researching and studying,
but **may not** use it in this assignment to directly answer questions and copy/paste results. As a reminder, the syllabus states
that you may be asked follow-up questions to explain the work you submitted and failure or a poor explanation as determined
by the instructor may result in points not being awarded. You are fully responsible for understanding how your programs
work. 

## Policy Reminder - Collaboration

For this assignment, you are allowed to collaborate with other students currently taking CSCI 1301
(cross-sectional) at Georgia Highlands College (see syllabus). This means that you may discuss the assignment, ask questions, and strategize with other students. However, you
are **not** allowed to copy and paste code from another student, your solutions must be your own.

You may also contact the instructor and ask questions or discuss the assignment with an official GHC tutor. If you would
like to discuss the assignment with anyone else, you must get the permission of the instructor first and may not do so
by default. For example, you may not collaborate with a friend who is a software engineer, a parent, sibling, or former
instructor at another institution unless given prior permission by the instructor. The intent of this policy is for
students to have access to the same resources to work on the problems and learn.

"""