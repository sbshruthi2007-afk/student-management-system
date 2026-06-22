from flask import Flask, render_template, request, flash, redirect
import csv
import requests

app = Flask(__name__)
app.secret_key = "secret123"


# Function to calculate average
def calculate_average(math, science, english):
    """Calculate average of three subjects."""
    return (int(math) + int(science) + int(english)) / 3


# Function to check duplicate student
def is_duplicate(name):
    """Check if student already exists."""
    try:
        with open('students.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header

            for row in reader:
                if row[0].strip().lower() == name.strip().lower():
                    return True
    except FileNotFoundError:
        return False

    return False

# Function to get motivational quote
def get_quote():
    """Fetch motivational quote from API."""
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        return data[0]['q']
    except:
        return "Keep going. Success comes with practice."


# Home page
@app.route('/')
def home():
    return render_template('add_student.html')


# Save student data
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    math = request.form['math']
    science = request.form['science']
    english = request.form['english']

    # Validation
    if name == "" or age == "" or math == "" or science == "" or english == "":
        flash("All fields are required!")
        return redirect('/')

    # Duplicate check
    if is_duplicate(name):
        flash("Student already exists!")
        return redirect('/')

    # Save into CSV
    with open('students.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, age, math, science, english])

    # Get quote
    quote = get_quote()

    return render_template('success.html', quote=quote)


# Leaderboard page
@app.route('/leaderboard')
def leaderboard():
    students = []

    with open('students.csv', 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            average = calculate_average(
                row['math'],
                row['science'],
                row['english']
            )

            row['average'] = average
            students.append(row)

    students.sort(key=lambda x: x['average'], reverse=True)

    return render_template('leaderboard.html', students=students)


# Custom 404 page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Custom 500 page
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


# Run app
if __name__ == '__main__':
    app.run(debug=True)