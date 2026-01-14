"""
Exercise Solutions for Module 1
Vibe Code Curriculum for Atomic Cat AI
"""

# Lesson 1.1 Exercises

print("=== Lesson 1.1: Introduction to Programming ===\n")

# Exercise 1: Hello, Vibe Code!
print("Hello, Vibe Code!")

# Exercise 2: Personal Greeting
print("Hello, my name is Atomic Cat!")


# Lesson 1.2 Exercises

print("\n=== Lesson 1.2: Variables and Data Types ===\n")

# Exercise 1: Personal Info
name = "Atomic Cat"
age = 5
favorite_color = "purple"
is_student = True

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Favorite Color: {favorite_color}")
print(f"Is Student: {is_student}")

# Exercise 2: Calculator
num1 = 15
num2 = 3

sum_result = num1 + num2
difference = num1 - num2
product = num1 * num2
quotient = num1 / num2

print(f"\n{num1} + {num2} = {sum_result}")
print(f"{num1} - {num2} = {difference}")
print(f"{num1} * {num2} = {product}")
print(f"{num1} / {num2} = {quotient}")

# Exercise 3: Temperature Converter
celsius = 25
fahrenheit = (celsius * 9/5) + 32
print(f"\n{celsius}°C = {fahrenheit}°F")


# Lesson 1.3 Exercises

print("\n=== Lesson 1.3: Control Flow and Logic ===\n")

# Exercise 1: Age Classifier
age = 30

if age <= 12:
    category = "Child"
elif age <= 19:
    category = "Teen"
elif age <= 64:
    category = "Adult"
else:
    category = "Senior"

print(f"Age {age} is classified as: {category}")

# Exercise 2: Number Guesser (simplified version)
secret_number = 7
guess = 7  # In a real version, this would be user input

attempts = 0
max_attempts = 5

while guess != secret_number and attempts < max_attempts:
    attempts += 1
    if guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
    # In a real program, we'd get new input here
    break

if guess == secret_number:
    print(f"Correct! You guessed it in {attempts} attempts!")

# Exercise 3: Multiplication Table
print("\nMultiplication Table for 5:")
number = 5
for i in range(1, 11):
    print(f"{number} × {i} = {number * i}")


# Lesson 1.4 Exercises

print("\n=== Lesson 1.4: Functions and Modularity ===\n")

# Exercise 1: Temperature Converter Function
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

temp_c = 30
temp_f = celsius_to_fahrenheit(temp_c)
print(f"{temp_c}°C = {temp_f}°F")

# Exercise 2: Calculator Functions
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
    if b != 0:
        return a / b
    else:
        return "Error: Division by zero"

print(f"\n10 + 5 = {add(10, 5)}")
print(f"10 - 5 = {subtract(10, 5)}")
print(f"10 * 5 = {multiply(10, 5)}")
print(f"10 / 5 = {divide(10, 5)}")

# Exercise 3: Email Validator
def is_valid_email(email):
    """Check if email is valid (basic validation)"""
    return '@' in email and '.' in email.split('@')[1]

test_emails = ["atomic@cat.ai", "invalid.email", "test@domain"]
print("\nEmail Validation:")
for email in test_emails:
    print(f"{email}: {is_valid_email(email)}")
