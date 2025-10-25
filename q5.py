# Write a python program to accept two numbers and display the quotient. Appropriate exception should be raised if the user enters the second number as zero.

try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    result = num1 / num2
    print("Quotient:", result)
except ZeroDivisionError:
    print("Division by zero is not allowed.")
