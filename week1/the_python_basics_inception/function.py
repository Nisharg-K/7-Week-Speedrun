# This is a simple calculator CLI made for implementing functions in python.
# Learning week 1, Topic 1.



def add(a,b):
    sum = a + b
    return sum

def subtract(a,b):
    difference = a - b
    return difference

def multiply(a,b):
    product = a * b
    return product  

def divide(a,b):
    quotient = a / b
    return quotient     

def modulo(a,b):
    remainder = a % b
    return remainder

print("\n Welcome to Calculator CLI, \n You can perform the following operations: \n 1. Addition \n 2. Subtraction \n 3. Multiplication \n 4. Division \n 5. Modulo")
n1 = int(input("Enter first number: "))
operator = input("Enter operator: ")
n2 = int(input("Enter second number: "))

res = 0


if operator == "+":
    res = add(n1,n2)

elif operator == "-":
    res = subtract(n1,n2)

elif operator == "*":
    res = multiply(n1,n2)

elif operator == "/":
    res = divide(n1,n2)

elif operator == "%":
    res = modulo(n1,n2)
else:
    print("Invalid operator")

print(f"{n1} {operator} {n2} = {res}")