# Write a python program to reverse a string using stack.

s = input("Enter string: ")
stack = []
for char in s:
    stack.append(char)

reversed_s = ""
while stack:
    reversed_s += stack.pop()

print("Original string:", s)
print("Reversed string:", reversed_s)
