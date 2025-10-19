# Write a python program to read a text file and count the number of vowels, consonants, uppercase and lowercase characters.

v = 0
c = 0
u = 0
l = 0

file = open("text.txt", "r")
for char in file.read():
    if char.islower():
        l += 1
        if char in "aeiou":
            v += 1
        else:
            c += 1
    elif char.isupper():
        u += 1
        if char in "AEIOU":
            v += 1
        else:
            c += 1

file.close()

print("Vowels:", v)
print("Consonants:", c)
print("Uppercase:", u)
print("Lowercase:", l)