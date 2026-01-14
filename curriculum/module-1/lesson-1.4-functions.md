# Lesson 1.4: Functions and Modularity

## Overview

Functions are reusable blocks of code that perform specific tasks. They help organize your code and avoid repetition.

## What are Functions?

A function is a named block of code that you can call multiple times:

```python
def greet():
    print("Hello, Vibe Code!")

# Call the function
greet()  # Output: Hello, Vibe Code!
```

## Function Parameters

Functions can accept input values (parameters):

```python
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Atomic Cat")  # Output: Hello, Atomic Cat!
greet_person("Felix")       # Output: Hello, Felix!
```

### Multiple Parameters

```python
def add_numbers(a, b):
    result = a + b
    print(f"{a} + {b} = {result}")

add_numbers(5, 3)  # Output: 5 + 3 = 8
```

## Return Values

Functions can return values:

```python
def multiply(x, y):
    return x * y

result = multiply(4, 5)
print(result)  # Output: 20
```

## Default Parameters

Set default values for parameters:

```python
def greet(name="friend", greeting="Hello"):
    print(f"{greeting}, {name}!")

greet()                           # Output: Hello, friend!
greet("Atomic Cat")              # Output: Hello, Atomic Cat!
greet("Felix", "Hi")             # Output: Hi, Felix!
```

## Keyword Arguments

Call functions using parameter names:

```python
def describe_pet(animal_type, pet_name):
    print(f"I have a {animal_type} named {pet_name}.")

describe_pet(animal_type="cat", pet_name="Whiskers")
describe_pet(pet_name="Rex", animal_type="dog")
```

## Variable Scope

Variables have different scopes:

```python
# Global variable
global_var = "I'm global!"

def my_function():
    # Local variable
    local_var = "I'm local!"
    print(global_var)  # Can access global
    print(local_var)   # Can access local

my_function()
# print(local_var)  # Error! Can't access local outside function
```

## Docstrings

Document your functions:

```python
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.
    
    Args:
        length: The length of the rectangle
        width: The width of the rectangle
        
    Returns:
        The area of the rectangle
    """
    return length * width
```

## Lambda Functions

Short, anonymous functions:

```python
# Regular function
def square(x):
    return x ** 2

# Lambda function
square_lambda = lambda x: x ** 2

print(square(5))         # Output: 25
print(square_lambda(5))  # Output: 25
```

## Exercise 1: Temperature Converter Function

Create a function that converts Celsius to Fahrenheit:

```python
# Your code here
def celsius_to_fahrenheit(celsius):
    # Convert and return the result
    pass
```

## Exercise 2: Calculator Functions

Create a calculator with separate functions for each operation:

```python
# Your code here
def add(a, b):
    pass

def subtract(a, b):
    pass

def multiply(a, b):
    pass

def divide(a, b):
    pass
```

## Exercise 3: Email Validator

Create a function that checks if an email is valid:

```python
# Your code here
def is_valid_email(email):
    # Check if email contains @ and .
    pass
```

## Key Takeaways

- Functions organize code into reusable blocks
- Parameters pass data into functions
- Return values send data back from functions
- Default parameters provide fallback values
- Scope determines where variables can be accessed
- Docstrings document your functions
- Lambda functions create short anonymous functions

## Module 1 Complete!

Congratulations! You've completed Module 1. You now understand:
- Basic programming concepts
- Variables and data types
- Control flow and logic
- Functions and modularity

Continue to Module 2 to learn about data structures and algorithms!
