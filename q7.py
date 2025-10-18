# Write a python program to perform read and write operation in a text file.

file = open("text.txt", "w")
data = file.write("Hello")
file.close()

file = open("text.txt", "r")
data = file.read()
print(data)
file.close()