# Write a python program to search for a specific word in a text file.

word = "hello"

file = open("text.txt", "r")
for line in file.readlines():
    if word in line:
        print("Found")
        break
        
else:
    print("Not found")

file.close()