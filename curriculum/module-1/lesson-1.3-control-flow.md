# Lesson 1.3: Control Flow and Logic

## Overview

Control flow allows your programs to make decisions and repeat actions. This is what makes programs truly powerful!

## Conditional Statements

### If Statements

The `if` statement allows you to execute code only when a condition is true:

```python
age = 18

if age >= 18:
    print("You are an adult!")
```

### If-Else Statements

Add an `else` clause to handle the alternative:

```python
temperature = 75

if temperature > 80:
    print("It's hot outside!")
else:
    print("It's nice outside!")
```

### If-Elif-Else Statements

Use `elif` for multiple conditions:

```python
score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")
```

## Comparison Operators

- `==` : Equal to
- `!=` : Not equal to
- `>` : Greater than
- `<` : Less than
- `>=` : Greater than or equal to
- `<=` : Less than or equal to

```python
x = 10
y = 20

print(x == y)  # False
print(x < y)   # True
print(x != y)  # True
```

## Logical Operators

Combine multiple conditions:

### AND (`and`)
Both conditions must be true:
```python
age = 25
has_license = True

if age >= 18 and has_license:
    print("You can drive!")
```

### OR (`or`)
At least one condition must be true:
```python
is_weekend = True
is_holiday = False

if is_weekend or is_holiday:
    print("Time to relax!")
```

### NOT (`not`)
Reverses the condition:
```python
is_raining = False

if not is_raining:
    print("Let's go for a walk!")
```

## Loops

### While Loops

Repeat code while a condition is true:

```python
count = 1

while count <= 5:
    print(f"Count: {count}")
    count += 1
```

### For Loops

Iterate over a sequence:

```python
# Loop through a range
for i in range(5):
    print(f"Number: {i}")

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

## Break and Continue

### Break
Exit the loop early:
```python
for i in range(10):
    if i == 5:
        break
    print(i)  # Prints 0-4
```

### Continue
Skip to the next iteration:
```python
for i in range(5):
    if i == 2:
        continue
    print(i)  # Prints 0, 1, 3, 4
```

## Exercise 1: Age Classifier

Write a program that classifies age into categories:

```python
# Your code here
# Child (0-12), Teen (13-19), Adult (20-64), Senior (65+)
age = 30
```

## Exercise 2: Number Guesser

Create a simple number guessing game:

```python
# Your code here
# Use a while loop to let the user guess until they get it right
secret_number = 7
```

## Exercise 3: Multiplication Table

Print the multiplication table for a given number:

```python
# Your code here
# Use a for loop to print the multiplication table for number 5
number = 5
```

## Key Takeaways

- `if`/`elif`/`else` statements make decisions
- Comparison operators compare values
- Logical operators combine conditions
- `while` loops repeat while a condition is true
- `for` loops iterate over sequences
- `break` and `continue` control loop execution

## Next Steps

Continue to Lesson 1.4 to learn about functions and modularity!
