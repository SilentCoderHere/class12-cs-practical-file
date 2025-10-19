# Write a python program to search for a specific record in a binary file based on given key (example: roll number).

import pickle

students = [
    {"rollno": 1, "name": "Abc", "class": 12},
    {"rollno": 2, "name": "Pqr", "class": 12},
    {"rollno": 3, "name": "Xyz", "class": 12}
]

file = open("students.dat", "wb")
pickle.dump(students, file)
file.close()

key = 2
file = open("students.dat", "rb")
data = pickle.load(file)
file.close()

for student in data:
    if student["rollno"] == key:
        print("Record found:", student)
        break
else:
    print("Record not found")