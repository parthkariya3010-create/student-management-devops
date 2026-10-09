
import os
import sqlite3
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
DB_PATH = os.getenv("DB_PATH", "students.db")

COURSES = [
    "Computer Science",
    "Information Technology",
    "Mechanical Engineering",
    "Electronics & Communication",
    "Civil Engineering",
    "AIML",
    "Data Science"
]


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    folder = os.path.dirname(DB_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                course TEXT NOT NULL
            )
        """)

        # Add new columns safely when upgrading an older database.
        columns = {
            row["name"]
            for row in db.execute("PRAGMA table_info(students)")
        }

        for column, definition in [
            ("email", "TEXT NOT NULL DEFAULT ''"),
            ("gender", "TEXT NOT NULL DEFAULT 'Male'"),
            ("status", "TEXT NOT NULL DEFAULT 'Active'")
        ]:
            if column not in columns:
                db.execute(
                    f"ALTER TABLE students ADD COLUMN {column} {definition}"
                )


@app.route("/")
def index():
    with get_db() as db:
        students = db.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

        total = db.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        male = db.execute(
            "SELECT COUNT(*) FROM students WHERE gender = 'Male'"
        ).fetchone()[0]

        female = db.execute(
            "SELECT COUNT(*) FROM students WHERE gender = 'Female'"
        ).fetchone()[0]

        course_count = db.execute(
            "SELECT COUNT(DISTINCT course) FROM students"
        ).fetchone()[0]

        edit_id = request.args.get("edit", type=int)
        editing = None

        if edit_id:
            editing = db.execute(
                "SELECT * FROM students WHERE id = ?", (edit_id,)
            ).fetchone()

    return render_template(
        "index.html",
        students=students,
        total=total,
        male=male,
        female=female,
        course_count=course_count,
        courses=COURSES,
        editing=editing
    )


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    course = request.form.get("course", "").strip()
    gender = request.form.get("gender", "").strip()

    if not name or not email or course not in COURSES:
        flash("Please complete all required fields.", "error")
        return redirect(url_for("index"))

    if gender not in ("Male", "Female"):
        flash("Please select a valid gender.", "error")
        return redirect(url_for("index"))

    with get_db() as db:
        existing = db.execute(
            "SELECT id FROM students WHERE lower(email) = lower(?)",
            (email,)
        ).fetchone()

        if existing:
            flash("That email address is already registered.", "error")
            return redirect(url_for("index"))

        db.execute("""
            INSERT INTO students (name, email, course, gender, status)
            VALUES (?, ?, ?, ?, 'Active')
        """, (name, email, course, gender))

    flash(f"{name} was added successfully.", "success")
    return redirect(url_for("index"))


@app.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    course = request.form.get("course", "").strip()
    gender = request.form.get("gender", "").strip()

    if not name or not email or course not in COURSES:
        flash("Please complete all required fields.", "error")
        return redirect(url_for("index", edit=student_id))

    if gender not in ("Male", "Female"):
        flash("Please select a valid gender.", "error")
        return redirect(url_for("index", edit=student_id))

    with get_db() as db:
        duplicate = db.execute("""
            SELECT id FROM students
            WHERE lower(email) = lower(?) AND id != ?
        """, (email, student_id)).fetchone()

        if duplicate:
            flash("Another student is already using that email.", "error")
            return redirect(url_for("index", edit=student_id))

        cursor = db.execute("""
            UPDATE students
            SET name = ?, email = ?, course = ?, gender = ?
            WHERE id = ?
        """, (name, email, course, gender, student_id))

        if cursor.rowcount == 0:
            flash("Student record not found.", "error")
        else:
            flash("Student details updated successfully.", "success")

    return redirect(url_for("index"))


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db() as db:
        db.execute("DELETE FROM students WHERE id = ?", (student_id,))

    flash("Student record deleted.", "success")
    return redirect(url_for("index"))


@app.route("/health")
def health():
    try:
        with get_db() as db:
            db.execute("SELECT 1").fetchone()
        return jsonify(status="healthy", database="connected"), 200
    except sqlite3.Error:
        return jsonify(status="unhealthy", database="error"), 500


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
