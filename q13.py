# Write a python program to create a CSV file, perform read and write operations in CSV file using user defined functions.

import csv


def create_csv(filename, data):
    file = open(filename, "w", newline="")
    writer = csv.writer(file)
    writer.writerows(data)
    file.close()


def write_csv(filename, row):
    file = open(filename, "a", newline="")
    writer = csv.writer(file)
    writer.writerow(row)
    file.close()


def read_csv(filename):
    file = open(filename, "r")
    reader = csv.reader(file)
    for row in reader:
        print(row)
    file.close()


create_csv("data.csv", [["Name", "Age"], ["Prem", 20], ["Jay", 30]])
write_csv("data.csv", ["Sarthak", 40])
read_csv("data.csv")
