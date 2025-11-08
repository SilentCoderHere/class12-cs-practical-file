# Write a python program to connect to a database to delete a student record based on their roll no from the ‘Students’ table.

import mysql.connector as sql

con = sql.connect(host="localhost", user="root", password="password", database="School")

cur = con.cursor()

cur.execute("DELETE FROM Students WHERE rollno = 1")

con.commit()
con.close()
