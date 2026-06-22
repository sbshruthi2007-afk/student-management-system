# student-management-system
capstone project
Student Management System (Flask Web Application)

Overview
This is a Flask-based web application designed to manage student records efficiently. It supports adding students, storing records in CSV format, displaying a leaderboard based on average scores, and includes form validation, motivational quote integration, and custom error handling pages.

Features
- Add student details through a web form
- Store student records in CSV file
- Prevent duplicate student entries
- Display leaderboard based on student average scores
- Integrate motivational quote API
- Form validation with flash messages
- Custom 404 and 500 error pages
- Unit testing using unittest framework
- GitHub Actions CI for automated testing

Technologies Used
- Python
- Flask
- HTML
- CSV
- Requests library

Project Structure
student-management-system/
│
├── templates/
│   ├── add_student.html
│   ├── leaderboard.html
│   ├── error_404.html
│   ├── error_500.html
│
├── student_form.py
├── students.csv
├── test_app.py
├── README.md

Installation and Setup

1. Clone the repository
git clone https://github.com/your-username/student-management-system.git

2. Navigate to project folder
cd student-management-system

3. Install dependencies
pip install flask requests

4. Run the application
python student_form.py

How to Use
1. Run the Flask application
2. Open browser and go to http://127.0.0.1:5000
3. Add student details using the form
4. View student leaderboard
5. Check validation messages and rankings

Testing
Run unit tests using:
python -m unittest test_app.py

CI/CD
This project uses GitHub Actions for continuous integration to automatically run tests on every push.

Future Improvements
- Add database support (MySQL or PostgreSQL)
- Add login and authentication system
- Improve UI using Bootstrap
- Add edit/update student feature

Version
v1.0

Author
Shruthi S B