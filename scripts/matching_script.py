import sqlite3, os

conn = sqlite3.connect("/Users/williamhoman/PycharmProjects/Project_wazevedo/data/assignments.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM problems ORDER BY position LIMIT 1 OFFSET 3")
row = dict(cursor.fetchone())
conn.close()

base = "/Users/williamhoman/PycharmProjects/Project_wazevedo"

for k, v in row.items():
    if k == "instructions" and v:
        full_path = os.path.join(base, v)
        print(f"\n=== instructions (from {v}) ===")
        with open(full_path) as f:
            print(f.read())
    elif k == "unit_tests" and v:
        full_path = os.path.join(base, v)
        print(f"\n=== unit_tests (from {v}) ===")
        with open(full_path) as f:
            print(f.read())
    elif k == "src_code" and v:
        full_path = os.path.join(base, v)
        print(f"\n=== src_code (from {v}) ===")
        with open(full_path) as f:
            print(f.read())
    else:
        print(f"\n=== {k} ===\n{v}")