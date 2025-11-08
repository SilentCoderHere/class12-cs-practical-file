# Write a python program to connect to a database and insert 5 records into the ‘Students’ table.

import mysql.connector as sql

con = sql.connect(host="localhost", user="root", password="password", database="School")

cur = con.cursor()

cur.execute("INSERT INTO Students(rollno, name, class) VALUES(1, 'Rohit', 8)")
cur.execute("INSERT INTO Students(rollno, name, class) VALUES(2, 'Mohit', 4)")
cur.execute("INSERT INTO Students(rollno, name, class) VALUES(3, 'Prem', 12)")
cur.execute("INSERT INTO Students(rollno, name, class) VALUES(4, 'Pankaj', 7)")
cur.execute("INSERT INTO Students(rollno, name, class) VALUES(5, 'Ravi', 6)")

con.commit()
con.close()
