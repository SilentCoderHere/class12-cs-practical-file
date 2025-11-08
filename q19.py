# Write a python program to connect to a database to fetch and display all student records from the ‘Students’ table.

import mysql.connector as sql

con = sql.connect(host="localhost", user="root", password="password", database="School")

cur = con.cursor()

cur.execute("SELECT * FROM Students")

data = cur.fetchall()

for student in data:
    print("Roll No:", student[0])
    print("Name:", student[1])
    print("Class:", student[2])
    print()
