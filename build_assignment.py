import sqlite3

def create_assignment(assignment_id, title, topics, db_name='assignments.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Insert new assignment
    c.execute("INSERT OR IGNORE INTO assignments (id, title) VALUES (?, ?)", (assignment_id, title))

    # Search problems by topic
    placeholders = ','.join('?' for _ in topics)
    query = f"SELECT id FROM problems WHERE topic IN ({placeholders})"
    c.execute(query, topics)
    problem_ids = [row[0] for row in c.fetchall()]

    # Link problems
    for pid in problem_ids:
        c.execute(
            "INSERT OR IGNORE INTO assignment_problems (assignment_id, problem_id) VALUES (?, ?)",
            (assignment_id, pid)
        )

    conn.commit()
    conn.close()

    print(f"Assignment '{title}' created with problems: {problem_ids}")

# No example usage here!