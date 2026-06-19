from flask import Flask, render_template, request, redirect
import sqlite3
from models.db import init_db

app = Flask(__name__)

init_db()


@app.route("/")
def home():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template("add_student.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    age = request.form["age"]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)",
        (name, age)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_student(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)