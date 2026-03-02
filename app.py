from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

# GitLab helper
from gitlab_utils import list_problem_folders

# Flask app
app = Flask(__name__)
app.secret_key = "dev-secret-key"


# Creates home page
@app.route("/")
def home():
    return render_template("index.html")


# Creates view assignments component
@app.route("/assignments")
def assignments():
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("SELECT id, title FROM assignments")
    rows = c.fetchall()
    conn.close()
    return render_template("assignments.html", assignments=rows)


# Creates the assignments for the web app

@app.route("/create", methods=["POST"])
def create():
    title = request.form["title"]
    assignment_id = "A" + title[:3].upper()

    create_assignment(assignment_id, title, [])

    flash("Assignment created successfully!")
    return redirect(url_for('home'))



# Supposed to display the problems from gitlab, however not figured out yet

import os

@app.route("/problems")
def problems():
    base_dir = "cs2-problem-repo"  # problem directory

    # List directories inside problems file
    if not os.path.exists(base_dir):
        return "No problems folder found."

    folders = []
    for name in os.listdir(base_dir):
        path = os.path.join(base_dir, name)
        if os.path.isdir(path):
            folders.append({"name": name, "path": path})

    return render_template("problems.html", problems=folders)


# Links assignments to assignment builder

@app.route("/link", methods=["POST"])
def link():
    assignment_id = request.form["assignment_id"]
    problem_id = request.form["problem_id"]

    conn = sqlite3.connect("assignments.db")
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
