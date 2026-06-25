from flask import Flask, render_template, request, flash, redirect, session, url_for
import sqlite3
import requests
import re   # ✅ ADDED for email validation

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------- EMAIL VALIDATION ----------------

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


# ---------------- DATABASE SETUP ----------------

def init_users_table():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def init_students_table():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            math INTEGER NOT NULL,
            science INTEGER NOT NULL,
            english INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def insert_sample_user():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        ''', ('Shruthi', 'shruthi@gmail.com', '1234'))
        conn.commit()
    except:
        pass

    conn.close()


# ---------------- HELPERS ----------------

def calculate_average(math, science, english):
    return (int(math) + int(science) + int(english)) / 3


def is_duplicate(name):
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM students WHERE name=?", (name,))
    exists = cursor.fetchone()

    conn.close()
    return exists is not None


def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=3)
        data = response.json()
        return data[0]['q']
    except:
        return "Keep going. Success comes with practice."


# ---------------- ROUTES ----------------

@app.route('/')
def landing():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')


@app.route('/add-student')
def add_student_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('add_student.html', username=session['username'])


@app.route('/add', methods=['POST'])
def add_student():
    if 'username' not in session:
        return redirect(url_for('login'))

    name = request.form['name']
    age = request.form['age']
    math = request.form['math']
    science = request.form['science']
    english = request.form['english']

    if not all([name, age, math, science, english]):
        flash("All fields are required!")
        return redirect(url_for('add_student_page'))

    if is_duplicate(name):
        flash("Student already exists!")
        return redirect(url_for('add_student_page'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO students (name, age, math, science, english)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, age, math, science, english))

    conn.commit()
    conn.close()

    quote = get_quote()
    return render_template('success.html', quote=quote)


@app.route('/leaderboard')
def leaderboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, age, math, science, english FROM students")
    rows = cursor.fetchall()
    conn.close()

    students = []

    for row in rows:
        students.append({
            'id': row[0],
            'name': row[1],
            'age': row[2],
            'math': row[3],
            'science': row[4],
            'english': row[5],
            'average': calculate_average(row[3], row[4], row[5])
        })

    students.sort(key=lambda x: x['average'], reverse=True)

    return render_template('leaderboard.html',
                           students=students,
                           username=session['username'])


@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute('''
            UPDATE students
            SET name=?, age=?, math=?, science=?, english=?
            WHERE id=?
        ''', (
            request.form['name'],
            request.form['age'],
            request.form['math'],
            request.form['science'],
            request.form['english'],
            student_id
        ))

        conn.commit()
        conn.close()

        flash("Student updated successfully ✏")
        return redirect(url_for('leaderboard'))

    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()
    conn.close()

    return render_template('edit_student.html', student=student)


@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()

    flash("Student deleted successfully ✅")
    return redirect(url_for('leaderboard'))


# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM users
            WHERE email=? AND password=?
        ''', (email, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            message = "Invalid Email or Password ❌"

    return render_template('login.html', message=message)


# ---------------- REGISTER (🔥 UPDATED) ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # ✅ EMAIL VALIDATION ADDED HERE
        if not is_valid_email(email):
            message = "Invalid email format ❌"
            return render_template('register.html', message=message)

        try:
            conn = sqlite3.connect('student.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            ''', (username, email, password))

            conn.commit()
            conn.close()

            return redirect(url_for('login'))

        except:
            message = "Email already exists ❌"

    return render_template('register.html', message=message)


# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=session['username'])


# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))


# ---------------- ERRORS ----------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# ---------------- RUN ----------------

if __name__ == '__main__':
    init_users_table()
    init_students_table()
    insert_sample_user()
    app.run(debug=True)