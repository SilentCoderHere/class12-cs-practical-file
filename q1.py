# Write a python program to calculate the factorial of a number using user defined functions.

def fact():
    f = 1
    n = int(input("Enter number: "))
    for i in range(1, n + 1):
        f *= i
        
    print("Factorial is", f)