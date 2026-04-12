from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import sqlite3
import csv
import io
from datetime import date, datetime

app = Flask(__name__)
DB = "attendance.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            class_name TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
            FOREIGN KEY (student_id) REFERENCES students(id),
            UNIQUE(student_id, date)
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
    today = date.today().isoformat()
    attendance_today = conn.execute(
        "SELECT student_id, status FROM attendance WHERE date = ?", (today,)
    ).fetchall()
    conn.close()
    att_map = {row["student_id"]: row["status"] for row in attendance_today}
    return render_template("index.html", students=students, att_map=att_map, today=today)

@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form["name"].strip()
    roll_no = request.form["roll_no"].strip()
    class_name = request.form["class_name"].strip()
    if name and roll_no and class_name:
        try:
            conn = get_db()
            conn.execute("INSERT INTO students (name, roll_no, class_name) VALUES (?, ?, ?)",
                         (name, roll_no, class_name))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            pass
    return redirect(url_for("index"))

@app.route("/delete_student/<int:sid>", methods=["POST"])
def delete_student(sid):
    conn = get_db()
    conn.execute("DELETE FROM attendance WHERE student_id = ?", (sid,))
    conn.execute("DELETE FROM students WHERE id = ?", (sid,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    data = request.get_json()
    today = date.today().isoformat()
    conn = get_db()
    for entry in data:
        conn.execute("""
            INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)
            ON CONFLICT(student_id, date) DO UPDATE SET status = excluded.status
        """, (entry["student_id"], today, entry["status"]))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Attendance saved!"})

@app.route("/report")
def report():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
    records = conn.execute("""
        SELECT s.name, s.roll_no, s.class_name, a.date, a.status
        FROM attendance a JOIN students s ON a.student_id = s.id
        ORDER BY a.date DESC, s.roll_no
    """).fetchall()

    # Stats per student
    stats = {}
    for s in students:
        row = conn.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) as present
            FROM attendance WHERE student_id = ?
        """, (s["id"],)).fetchone()
        total = row["total"] or 0
        present = row["present"] or 0
        pct = round((present / total * 100), 1) if total > 0 else 0
        stats[s["id"]] = {"total": total, "present": present, "pct": pct}

    conn.close()
    return render_template("report.html", students=students, records=records, stats=stats)

@app.route("/export_csv")
def export_csv():
    conn = get_db()
    records = conn.execute("""
        SELECT s.name, s.roll_no, s.class_name, a.date, a.status
        FROM attendance a JOIN students s ON a.student_id = s.id
        ORDER BY a.date DESC, s.roll_no
    """).fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Roll No", "Class", "Date", "Status"])
    for r in records:
        writer.writerow([r["name"], r["roll_no"], r["class_name"], r["date"], r["status"]])
    