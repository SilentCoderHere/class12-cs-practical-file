# Write a python program to implement a stack using list.

stack = []
MAX = 5

def push():
    element = input("Enter element: ")
    if len(stack) < MAX:
        stack.append(element)
        
    else:
        print("Stack overflow")
        
def pop():
    if len(stack) > 0:
        stack.pop()
    else:
        print("Stack underflow")