# 8. Write a python program to perform read and write operations in a binary file.

file = open("binary.dat", "wb")
data = file.write(b"Hello")
file.close()

file = open("binary.dat", "rb")
data = file.read()
print(data)
file.close()