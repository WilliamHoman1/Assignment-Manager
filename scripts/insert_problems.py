import sqlite3
# OLD
# Template for inserting sample problems into database, gets database set up

#def insert_sample_problems(db_name='assignments.db'):
   # conn = sqlite3.connect(db_name)
   # c = conn.cursor()

   # sample_problems = [
   #     ('P001', 'For Loop Basics', 'for loop', 'easy', 'python', 'instructions/P001.md', 'tests/P001_tests.py'),
   #     ('P002', 'While Loop Practice', 'while loop', 'medium', 'python', 'instructions/P002.md', 'tests/P002_tests.py'),
    #    ('P003', 'List Operations', 'lists', 'medium', 'python', 'instructions/P003.md', 'tests/P003_tests.py')
   # ]

  #  c.executemany('INSERT OR IGNORE INTO problems VALUES (?,?,?,?,?,?,?)', sample_problems)

  #  conn.commit()
  #  conn.close()
   # print("Sample problems inserted.")
#
#if __name__ == "__main__":
   # insert_sample_problems()


    # Insert problems from gitlab API

import gitlab
import sqlite3
import json
import os
from dotenv import load_dotenv
load_dotenv()
import sqlite3

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "assignments.db")

# GitLab Client

def get_gitlab_client():
    token = os.getenv("GITLAB_TOKEN")
    print("Token:", token)  # debug inside function
    if not token:
        raise Exception("GITLAB_TOKEN not set.")
    return gitlab.Gitlab("https://gitlab.com", private_token=token)

# GitLab Sync (Matches DB Schema)

def sync_gitlab_problems(project_id, metadata_filename="metadata.json", db_name=DB_PATH):
    gl = get_gitlab_client()
    project = gl.projects.get(project_id)

    # get all files (pagination-safe)
    items = project.repository_tree(recursive=True, get_all=True)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    synced = 0

    # inside sync_gitlab_problems

    for item in items:
        print(item)

        if item["type"] == "blob" and item["name"].endswith(".json"):

            file = project.files.get(file_path=item["path"], ref="main")
            content = file.decode().decode("utf-8")

            try:
                metadata = json.loads(content)
            except Exception as e:
                print(f"Skipping {item['path']} — invalid JSON: {e}")
                continue

            problem_id = metadata.get("id")
            title = metadata.get("title")
            topic = metadata.get("topic")
            difficulty = metadata.get("difficulty")
            language = metadata.get("language")

            instructions_path = metadata.get("instructions")
            position = metadata.get("position", 0)

            try:
                code_file = project.files.get(file_path=instructions_path, ref="main")
                instructions = code_file.decode().decode("utf-8")
            except Exception as e:
                print(f"Could not load instructions for {problem_id}: {e}")
                instructions = ""

            unit_tests = metadata.get("unit_tests")

            if not problem_id or not title:
                print(f"Skipping {item['path']} — missing id or title")
                continue

            cursor.execute("""
                INSERT OR REPLACE INTO problems
                (id, title, topic, difficulty, language, instructions, unit_tests, position)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                problem_id,
                title,
                topic,
                difficulty,
                language,
                instructions,
                unit_tests,
                position
            ))

            synced += 1

    conn.commit()
    conn.close()

    print(f"Synced {synced} problems from GitLab.")


# REMOVE THIS LATER
# TESTS PROBLEM EXISTENCE


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT id, title, LENGTH(instructions) FROM problems;")
for row in cursor.fetchall():
    print(row)

conn.close()

import sqlite3

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Set positions for ordering
cursor.execute("UPDATE problems SET position = 1 WHERE id = 'problem_one';")
cursor.execute("UPDATE problems SET position = 2 WHERE id = 'problem_two';")
cursor.execute("UPDATE problems SET position = 3 WHERE id = 'problem_three';")
cursor.execute("UPDATE problems SET position = 4 WHERE id = 'problem_four';")

conn.commit()
conn.close()

print("Positions updated.")
# test
#  Project ID : 79896930
if __name__ == "__main__":
    project_id = input("GitLab Project ID: ").strip()

    if not project_id:
        print("Project ID required.")
    else:
        sync_gitlab_problems(project_id)