# Write a python program to check whether the input number is prime or not using user defined functions.

def prime():
    n = int(input("Enter number: "))
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            print(n, "is not prime")
            break
    else:
        print(n, "is prime")
        
prime()