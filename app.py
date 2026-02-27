from flask import Flask, render_template
import sqlite3

# Flask web application
app = Flask(__name__)
# Flask requires a "secret key" to run (session handling)
app.secret_key = "dev-secret-key"

# Creates the home dashboard
@app.route("/")
def home():
    """Displays the home page."""
    return render_template("index.html")

# View assignments
@app.route("/assignments")
def assignments():
    """Reads from SQLite database and displays assignment ID and title"""
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()

    # Gets all assignments
    c.execute("SELECT id, title FROM assignments")
    rows = c.fetchall()

    conn.close()
    # Renders all of the assignments
    return render_template("assignments.html", assignments=rows)

from flask import request
from build_assignment import create_assignment

from flask import redirect, url_for, flash

# Creates the assignment route
@app.route("/create", methods=["POST"])
def create():
    """Receives title data, creates assignment ID, calls create_assignment
    to store in database. Then flash success message plays."""
    title = request.form["title"]
    # Generate simple assignment ID
    assignment_id = "A" + title[:3].upper()
    # Creates assignment in database
    create_assignment(assignment_id, title, [])
    # Shows success message/banner
    flash("Assignment created successfully!")
    return redirect(url_for('home'))


@app.route("/problems")
def problems():
    """Displays available problems that can be later linked to assignments
    with the linking method."""
    # Connect to database
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()

    # Search available problems
    c.execute("SELECT id, title, topic, difficulty FROM problems")
    rows = c.fetchall()

    # Close the connection
    conn.close()

    # Render the problems
    return render_template("problems.html", problems=rows)

@app.route("/link", methods=["POST"])
def link():
    """Links problems to assignments using the relational table(rows and columns).
    1. Receives assignment ID and title.
    2. Insert relationship
    3. Confirms linkage"""
    # Receive form data
    assignment_id = request.form["assignment_id"]
    problem_id = request.form["problem_id"]

    # Connect to database
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()

    # Insert relationship (Ignores duplicates)
    c.execute(
        "INSERT OR IGNORE INTO assignment_problems (assignment_id, problem_id) VALUES (?, ?)",
        (assignment_id, problem_id)
    )

    # Commit
    conn.commit()

    # Close
    conn.close()

    return "Linked!"

# Runs the server in development mode
if __name__ == "__main__":
    app.run(debug=True)