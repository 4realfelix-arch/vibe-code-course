"""
Calculator App - Solution
Vibe Code Curriculum Project 1
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        return "Error: Division by zero"
    return a / b

def get_number(prompt):
    """Get a valid number from user"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def calculator():
    """Main calculator function"""
    print("=" * 40)
    print("Welcome to Vibe Code Calculator!")
    print("=" * 40)
    
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }
    
    while True:
        print()
        num1 = get_number("Enter first number: ")
        
        op = input("Enter operation (+, -, *, /): ")
        while op not in operations:
            print("Invalid operation. Please use +, -, *, or /")
            op = input("Enter operation (+, -, *, /): ")
        
        num2 = get_number("Enter second number: ")
        
        result = operations[op](num1, num2)
        print(f"\nResult: {num1} {op} {num2} = {result}")
        
        continue_calc = input("\nContinue? (y/n): ").lower()
        if continue_calc != 'y':
            print("\nThank you for using Vibe Code Calculator!")
            break

if __name__ == "__main__":
    calculator()
