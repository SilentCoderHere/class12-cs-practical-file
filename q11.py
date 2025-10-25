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
        
while True:
    print("1. Push")
    print("2. Pop")
    print("3. Exit")
    
    choice = input("Enter: ")
    if choice == "1":
        push()
    elif choice == "2":
        pop()
    elif choice == "3":
        break
    else:
        print("Invalid")