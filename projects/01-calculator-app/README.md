# Project 1: Calculator App

## Description

Build a command-line calculator that can perform basic arithmetic operations.

## Requirements

1. Support addition, subtraction, multiplication, and division
2. Handle invalid input gracefully
3. Allow continuous calculations until user quits
4. Display clear error messages

## Features

- [x] Basic operations (+, -, *, /)
- [ ] Advanced operations (power, square root)
- [ ] History of calculations
- [ ] Save/load calculation history

## Getting Started

```python
# Starter code
def calculator():
    """Main calculator function"""
    print("Welcome to Vibe Code Calculator!")
    
    while True:
        # Your code here
        pass

if __name__ == "__main__":
    calculator()
```

## Example Output

```
Welcome to Vibe Code Calculator!

Enter first number: 10
Enter operation (+, -, *, /): +
Enter second number: 5
Result: 15

Continue? (y/n): y

Enter first number: 20
Enter operation (+, -, *, /): /
Enter second number: 4
Result: 5.0

Continue? (y/n): n
Thank you for using Vibe Code Calculator!
```

## Extensions

1. Add support for parentheses and order of operations
2. Implement memory functions (M+, M-, MR, MC)
3. Add support for complex expressions (e.g., "2 + 3 * 4")
4. Create a GUI version using tkinter
5. Add scientific calculator functions

## Learning Objectives

- Functions and modularity
- Input validation
- Error handling
- Control flow
- User interaction
