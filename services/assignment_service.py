

import sqlite3
import os
from dotenv import load_dotenv
import gitlab
import json

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

        for new_position, pid in enumerate(problem_ids, start=1):
            new_pid = f"problem_{new_position}"

            cursor.execute("""
                    SELECT instructions, unit_tests, src_code, supplemental_files
                    FROM problems
                    WHERE id = ?
                """, (pid,))
            row = cursor.fetchone()
            if not row:
                print(f"Problem {pid} not found in database, skipping.")
                continue

            instructions, tests, src_code, supplemental_files = row

            # Renumber content to match position in this assignment
            instructions = self._renumber_readme(instructions, pid, new_position)
            fixed_tests = self._fix_import(tests or "", new_pid)

            # Create problem folder with src and tests subdirectories
            problem_dir = os.path.join(export_dir, new_pid)
            src_dir = os.path.join(problem_dir, "src")
            tests_dir = os.path.join(problem_dir, "tests")
            os.makedirs(src_dir, exist_ok=True)
            os.makedirs(tests_dir, exist_ok=True)

            # Write problem README
            readme_path = os.path.join(problem_dir, "README.md")
            with open(readme_path, "w") as f:
                f.write(instructions or "")

            # Write source code into src/
            src_file_path = os.path.join(src_dir, f"{new_pid}.py")
            with open(src_file_path, "w") as f:
                f.write(src_code or "")

            # Write unit tests into tests/
            test_file_path = os.path.join(tests_dir, f"test_{new_pid}.py")
            with open(test_file_path, "w") as f:
                f.write(fixed_tests)

            # Write supplemental files into both src/ and tests/
            if supplemental_files:
                supp_data = json.loads(supplemental_files)
                for filename, content in supp_data.items():
                    for directory in [src_dir, tests_dir]:
                        supp_file_path = os.path.join(directory, filename)
                        with open(supp_file_path, "w") as f:
                            f.write(content)
        conn.close()

        # 4. Write root README
        root_readme_path = os.path.join(export_dir, "README.md")
        with open(root_readme_path, "w") as f:
            f.write(self.default_root_readme(problem_set_number))

        # 5. Push files to GitLab
        actions = []
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, export_dir)
                with open(file_path, "r") as f:
                    content = f.read()
                actions.append({
                    "action": "create",
                    "file_path": rel_path,
                    "content": content
                })

        try:
            project.commits.create({
                "branch": "main",
                "commit_message": f"Add Problem Set Lab {problem_set_number}",
                "actions": actions
            })
        except gitlab.exceptions.GitlabCreateError as e:
            print(f"Warning: Could not push files to GitLab: {e}")

        return project.web_url

    def _fix_import(self, test_code: str, problem_id: str) -> str:
        """
        Replace any 'import problem_xxx' style imports and class names with
        the actual problem file name so tests can find the source file.
        """
        import re
        # Replace import statement: import problem_three → import problem_1
        fixed = re.sub(r'import problem_\w+', f'import {problem_id}', test_code)

        # Replace function calls: problem_three.func() → problem_1.func()
        fixed = re.sub(r'problem_\w+\.', f'{problem_id}.', fixed)

        # Replace class name: TestProblemThree → TestProblem1
        fixed = re.sub(r'class TestProblem\w+\(', f'class Test{problem_id.capitalize()}(', fixed)

        return fixed

    def _renumber_readme(self, content: str, original_pid: str, new_position: int) -> str:
        """
        Replace hardcoded problem references in README with the new position number.
        e.g. problem_three → problem_1, Problem 3 → Problem 1
        """
        import re
        # Replace file path references: problem_three.py → problem_1.py
        content = content.replace(original_pid, f"problem_{new_position}")

        # Replace heading number: ## Problem 3 → ## Problem 1
        # Handles any digit that may already be there
        content = re.sub(
            r'(## Problem\s+)\d+',
            rf'\g<1>{new_position}',
            content
        )

        return content

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
we will focus on regular inline comments that start with a pound or hashtag sign (#) and docstrings, which are multiline
strings that go on the line right after the def keyword. 


Please note that unit tests relating to docstring are supportive in that they will test if you forgot
to update them and test if the docstring exists. But you need to check that you updated them as given
in the README.md directions.


## Important - Code Needs to Run As-Is - Please run and test before and after submitting.

As a reminder, your submitted code needs to run as-is. As per the syllabus, points may be deducted
for code that does not run up to and including earning 0 points. Please test your code before and after submitting.

For this assignment, a small and easily fixable issue as determined by the instructor (ex/ missing a colon, has a left
square bracket but not a right one, etc.) will result in a loss of -3pts per issue. If there is a significant issue that
would require major modification to fix as determined by the instructor for the program to run, it may result in no
points being awarded for the relevant components.


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

