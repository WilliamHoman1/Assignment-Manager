
import sqlite3
import gitlab
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "assignments.db")


def get_gitlab_client():
    """Pulls gitlab API"""
    token = os.getenv("GITLAB_TOKEN")
    if not token:
        raise Exception("GITLAB_TOKEN not set.")
    return gitlab.Gitlab("https://gitlab.com", private_token=token)


def sync_gitlab_problems(project_id):
    """Function that pulls the problems from GitLab into the database as JSON
    files, ready to be inserted into the database."""
    gl = get_gitlab_client()
    project = gl.projects.get(project_id)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    synced = 0

    items = project.repository_tree(recursive=True, get_all=True)

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
        supplemental_paths = metadata.get("supplemental_files", [])  # ← new

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

        # Fetch supplemental file contents and store by filename ← new
        supplemental_contents = {}
        for path in supplemental_paths:
            filename = os.path.basename(path)
            supplemental_contents[filename] = fetch_file(path, "supplemental")
        supplemental_json = json.dumps(supplemental_contents) if supplemental_contents else None

        if not problem_id or not title:
            print(f"Skipping {item['path']} — missing id or title")
            continue

        cursor.execute("""
            INSERT OR REPLACE INTO problems
            (id, title, topic, difficulty, language, instructions, unit_tests, src_code, position, supplemental_files)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            problem_id,
            title,
            topic,
            difficulty,
            language,
            instructions,
            unit_tests,
            src_code,
            position,
            supplemental_json  # ← new
        ))

        synced += 1

    conn.commit()
    conn.close()
    print(f"Synced {synced} problems from GitLab.")

def main():
    """To run the insertion of problems into the database. The project ID
    is needed for this to be completed. Project ID is attached below."""
    project_id = input("GitLab Project ID: ").strip()
    if not project_id:
        print("Project ID required.")
        return
    sync_gitlab_problems(project_id)

# Project ID: 79896930
if __name__ == "__main__":
    main()