# Lesson 1.2: Variables and Data Types

## Overview

Variables are containers that store data values. Think of them as labeled boxes where you can put information.

## What are Variables?

A variable is a name that refers to a value. In Python, you create a variable by assigning it a value:

```python
name = "Atomic Cat"
age = 5
is_ai = True
```

## Data Types

Python has several basic data types:

### 1. Strings (str)
Text data, enclosed in quotes:
```python
message = "Hello, World!"
name = 'Atomic Cat'
```

### 2. Integers (int)
Whole numbers:
```python
age = 25
year = 2026
```

### 3. Floats (float)
Decimal numbers:
```python
temperature = 72.5
pi = 3.14159
```

### 4. Booleans (bool)
True or False values:
```python
is_active = True
is_complete = False
```

## Variable Naming Rules

1. Must start with a letter or underscore
2. Can contain letters, numbers, and underscores
3. Case-sensitive (`name` and `Name` are different)
4. Use descriptive names

### Good Examples:
```python
user_name = "Felix"
total_count = 100
is_valid = True
```

### Bad Examples:
```python
x = "Felix"  # Not descriptive
1name = "Felix"  # Starts with number (error!)
user-name = "Felix"  # Uses hyphen (error!)
```

## Using Variables

```python
# Creating variables
first_name = "Atomic"
last_name = "Cat"

# Using variables
full_name = first_name + " " + last_name
print(full_name)  # Output: Atomic Cat

# Updating variables
age = 5
age = age + 1
print(age)  # Output: 6
```

## Type Conversion

You can convert between data types:

```python
# String to integer
age_string = "25"
age_number = int(age_string)

# Integer to string
count = 100
count_string = str(count)

# String to float
price = float("19.99")
```

## Exercise 1: Personal Info

Create variables for your personal information and print them:

```python
# Your code here
# Create variables for: name, age, favorite_color, is_student
```

## Exercise 2: Calculator

Create a simple calculator using variables:

```python
# Your code here
# Create two numbers and calculate their sum, difference, product, and quotient
```

## Exercise 3: Temperature Converter

Convert Celsius to Fahrenheit using the formula: F = (C × 9/5) + 32

```python
# Your code here
celsius = 25
# Calculate fahrenheit
```

## Key Takeaways

- Variables store data values
- Python has multiple data types: strings, integers, floats, booleans
- Use descriptive variable names
- You can convert between data types
- Variables can be updated and reused

## Next Steps

Continue to Lesson 1.3 to learn about control flow and logic!
