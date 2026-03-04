from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os # Interact with operating system
import uuid # Generates unique ID's for assignments to differentiate
from build_assignment import create_assignment

# Flask (website) setup
app = Flask(__name__)
app.secret_key = "dev-secret-key"

# Path to directory of database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Path to database
DB_PATH = os.path.join(BASE_DIR, "assignments.db")


# Home
@app.route("/")
def home():
    """Calls index.html"""
    return render_template("index.html")


# View assignments (use row id or id)
@app.route("/assignments")
def assignments():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Use row id (auto number) instead of long UUID
    c.execute("SELECT rowid, title FROM assignments")
    rows = c.fetchall()

    conn.close()

    return render_template("assignments.html", assignments=rows)

# Create assignment ( unique ID)
@app.route("/create", methods=["POST"])
def create():
    title = request.form["title"]

    # Generate truly unique ID
    assignment_id = str(uuid.uuid4())

    # Insert using DB path
    create_assignment(assignment_id, title, [], db_name=DB_PATH)

    flash("Assignment created successfully!")
    return redirect(url_for('assignments'))


@app.route("/problems")
def problems():
    conn = sqlite3.connect("assignments.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, topic, difficulty, language, instructions, position
        FROM problems
        ORDER BY position ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    # prepare for template
    problems = []
    for row in rows:
        problems.append({
            "id": row["id"],
            "title": row["title"],
            "topic": row["topic"],
            "difficulty": row["difficulty"],
            "language": row["language"],
            "position": row["position"],
            "preview": row["instructions"][:300] + "..." if row["instructions"] else ""
        })

    return render_template("problems.html", problems=problems)

# Link assignment to problem
@app.route("/link", methods=["POST"])
def link():
    assignment_id = request.form["assignment_id"]
    problem_id = request.form["problem_id"]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT OR IGNORE INTO assignment_problems (assignment_id, problem_id) VALUES (?, ?)",
        (assignment_id, problem_id)
    )

    conn.commit()
    conn.close()

    return "Linked!"

@app.route("/problems")
def show_problems():
    conn = sqlite3.connect("assignments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM problems")
    problems = cursor.fetchall()
    conn.close()

    return render_template("problems.html", problems=problems)

@app.route("/problem/<problem_id>")
def view_problem(problem_id):
    conn = sqlite3.connect("assignments.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, topic, difficulty, language, instructions
        FROM problems
        WHERE id = ?
    """, (problem_id,))

    problem = cursor.fetchone()
    conn.close()

    if not problem:
        return "Problem not found.", 404

    return render_template("view_problem.html", problem=problem)

if __name__ == "__main__":
    app.run(debug=True)
