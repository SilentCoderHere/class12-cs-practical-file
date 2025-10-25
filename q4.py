# Write a python program to swap 2 numbers without using third variable and by using third variable through user defined functions.

def swap_without_third():
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    
    a = a + b
    b = a - b
    a = a - b
    
    print("a:", a)
    print("b:", b)
    
def swap_with_third():
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    
    temp = a
    a = b
    b = temp
    
    print("a:", a)
    print("b:", b)
    
swap_without_third()
swap_with_third()