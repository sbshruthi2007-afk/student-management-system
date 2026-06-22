import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM students")
print(cursor.fetchall())

conn.close()