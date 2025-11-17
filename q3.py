# Write a python program to design a simple calculator using user defined functions.


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

choice = input("Enter choice (+, -, *, /): ")

if choice == "+":
    print(add(a, b))
elif choice == "-":
    print(subtract(a, b))
elif choice == "*":
    print(multiply(a, b))
elif choice == "/":
    print(divide(a, b))
else:
    print("Invalid choice")
