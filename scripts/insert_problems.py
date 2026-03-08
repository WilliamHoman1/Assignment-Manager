
import sqlite3
import gitlab
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "assignments.db")


def get_gitlab_client():
    token = os.getenv("GITLAB_TOKEN")
    if not token:
        raise Exception("GITLAB_TOKEN not set.")
    return gitlab.Gitlab("https://gitlab.com", private_token=token)


def sync_gitlab_problems(project_id):
    gl = get_gitlab_client()
    project = gl.projects.get(project_id)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    synced = 0

    # Iterate over JSON metadata files in the repo
    items = project.repository_tree(recursive=True, get_all=True)
    items = project.repository_tree(recursive=True, get_all=True)

    # DEBUG: print all paths GitLab sees
    for item in items:
        print(item["path"], item["type"])

    for item in items:
        if item["type"] != "blob" or not item["name"].endswith(".json"):
            continue

        try:
            file = project.files.get(file_path=item["path"], ref="main")
            content = file.decode().decode("utf-8")
            metadata = json.loads(content)
        except Exception as e:
            print(f"Skipping {item['path']} — invalid JSON or GitLab fetch error: {e}")
            continue

        problem_id = metadata.get("id")
        title = metadata.get("title")
        topic = metadata.get("topic")
        difficulty = metadata.get("difficulty")
        language = metadata.get("language")
        position = metadata.get("position", 0)

        instructions_path = metadata.get("instructions")
        code_path = metadata.get("code")
        tests_path = metadata.get("unit_tests")

        # Fetch instructions, src, and tests from GitLab
        def fetch_file(path, file_type):
            if not path:
                return ""
            try:
                f = project.files.get(file_path=path, ref="main")
                return f.decode().decode("utf-8")
            except gitlab.exceptions.GitlabGetError:
                print(f"Could not load {file_type} for {problem_id}: 404")
                return ""

        instructions = fetch_file(instructions_path, "instructions")
        src_code = fetch_file(code_path, "src")
        unit_tests = fetch_file(tests_path, "tests")

        if not problem_id or not title:
            print(f"Skipping {item['path']} — missing id or title")
            continue

        cursor.execute("""
            INSERT OR REPLACE INTO problems
            (id, title, topic, difficulty, language, instructions, unit_tests, src_code, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            problem_id,
            title,
            topic,
            difficulty,
            language,
            instructions,
            unit_tests,
            src_code,
            position
        ))

        synced += 1

    conn.commit()
    conn.close()
    print(f"Synced {synced} problems from GitLab.")


def main():
    project_id = input("GitLab Project ID: ").strip()
    if not project_id:
        print("Project ID required.")
        return
    sync_gitlab_problems(project_id)

# Project ID: 79896930
if __name__ == "__main__":
    main()