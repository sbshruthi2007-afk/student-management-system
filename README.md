Student Management System

A full-stack web application developed using Flask, HTML, CSS, and SQLite to manage student records efficiently. This project provides a structured system for user authentication, student data management, leaderboard tracking, and performance monitoring.

Project Overview

The Student Management System is designed to simplify the process of storing and managing student information through an interactive web interface. It allows users to register, log in, view dashboards, manage student records, and track rankings through a leaderboard system.

Features

• User Registration and Login Authentication
• Session Management
• Dashboard Interface
• Student Record Management
• Leaderboard Ranking System
• Form Validation
• Error and Success Notifications
• API Integration
• Responsive and Modern User Interface

Technologies Used
Frontend
HTML
CSS
Backend
Python
Flask
Database
SQLite
Project Structure

Student-Management-System
│── app.py
│── requirements.txt
│── README.md
│── student.db

templates/
• login.html
• register.html
• dashboard.html
• leaderboard.html

static/
• style.css

Installation and Setup
Clone the repository from GitHub.
Open the project folder in your preferred code editor.
Install the required dependencies using the requirements file.
Run the Flask application.
Open the application in your browser using the local server address.
Workflow

The system follows a simple workflow:

User accesses the login page.
User enters login credentials.
Flask receives the form data and processes the request.
The system validates the data using SQLite database.
If the credentials are valid, the user is redirected to the dashboard.
If invalid, an error message is displayed.
Student records are managed and leaderboard scores are updated accordingly.
Core Concepts Implemented
Flask Routing
Request and Response Handling
Session Management
Database Integration
Form Handling
Flash Messaging
Page Redirection
API Integration
Future Enhancements
Secure password hashing
Admin panel integration
Advanced analytics dashboard
Export reports to CSV/PDF
Improved UI/UX design
Search and filter functionality
Author

Shruthi S B