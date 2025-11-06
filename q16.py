# Write a python program to connect to a database and create a table named ‘Students’ with attributes ‘Roll No, Name, and Class’.

import mysql.connector as sql

con = sql.connect(
    host="localhost",
    user="root",
    password="password",
    database="School"
)

cur = con.cursor()

cur.execute("CREATE TABLE Students(rollno INT, name VARCHAR(30), class INT)")

con.commit()
cur.close()
con.close()
