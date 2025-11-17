# Write a python program to perform read and write operation in a text file.

file = open("text.txt", "w+")
file.write("Hello")
print("Data saved")
data = file.read()
print("Data read:", data)
file.close()
