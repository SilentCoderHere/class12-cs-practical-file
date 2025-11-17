# 8. Write a python program to perform read and write operations in a binary file.

file = open("binary.dat", "wb")
data = file.write(b"Hello")
print("Binary data saved")

file.close()

file = open("binary.dat", "rb")
data = file.read()
print("Data read:", data)

file.close()
