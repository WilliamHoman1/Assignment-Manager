import shutil
import os
import sqlite3

def export_assignment(assignment_id, db_name='assignments.db'):
    """Template for bundling assignment into database along with problems

    Function: Combining desired assignments into problem set using assignment ID's
    Does not explicitly do anything currently, just here as setup for later."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT title FROM assignments WHERE id=?", (assignment_id,))
    row = c.fetchone()

    if row is None:
        print(f"Assignment {assignment_id} not found.")
        conn.close()
        return

    title = row[0]

    c.execute("SELECT problem_id FROM assignment_problems WHERE assignment_id=?", (assignment_id,))
    problem_ids = [row[0] for row in c.fetchall()]

    os.makedirs(title, exist_ok=True)

    for pid in problem_ids:
        c.execute("SELECT instructions, unit_tests FROM problems WHERE id=?", (pid,))
        result = c.fetchone()

        if not result:
            continue

        instr, tests = result

        # Copy only if file exists
        if instr and os.path.exists(instr):
            shutil.copy(instr, title)
        else:
            print(f"Instruction file missing: {instr}")

        if tests and os.path.exists(tests):
            shutil.copy(tests, title)
        else:
            print(f"Test file missing: {tests}")

    conn.close()
    print(f"Assignment exported to folder: {title}")