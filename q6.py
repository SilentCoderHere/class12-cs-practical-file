# 6. Write a python program to catch the IndexError exception in sequence data type(string, list, tuples).

t = (1, 2, 3, 4)
i = int(input("Enter idex: "))
try:
    value = t[i]
    print(value)
        
except IndexError:
    print("Out of range")