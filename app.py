from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
import uuid
from build_assignment import create_assignment

# Flask setup
app = Flask(__name__)
app.secret_key = "dev-secret-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "assignments.db")


# Home
@app.route("/")
def home():
    return render_template("index.html")


# View assignments (use rowid or id)
@app.route("/assignments")
def assignments():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Use rowid (auto number) instead of long UUID
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


# View problems (local)
@app.route("/problems")
def problems():
    base_dir = os.path.join(BASE_DIR, "cs2-problem-repo")

    if not os.path.exists(base_dir):
        return "No problems folder found."

    folders = []
    for name in os.listdir(base_dir):
        path = os.path.join(base_dir, name)
        if os.path.isdir(path):
            folders.append({"name": name, "path": path})

    return render_template("problems.html", problems=folders)


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


if __name__ == "__main__":
    app.run(debug=True)
