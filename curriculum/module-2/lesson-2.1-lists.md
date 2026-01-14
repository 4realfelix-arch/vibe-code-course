# Lesson 2.1: Arrays and Lists

## Overview

Lists are one of the most versatile data structures in Python. They allow you to store multiple items in a single variable.

## What are Lists?

A list is an ordered collection of items:

```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]
```

## Accessing List Elements

Use indexing to access elements (starting at 0):

```python
fruits = ["apple", "banana", "cherry"]

print(fruits[0])   # Output: apple
print(fruits[1])   # Output: banana
print(fruits[-1])  # Output: cherry (last item)
```

## List Slicing

Get a portion of a list:

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:5])    # Output: [2, 3, 4]
print(numbers[:3])     # Output: [0, 1, 2]
print(numbers[5:])     # Output: [5, 6, 7, 8, 9]
print(numbers[::2])    # Output: [0, 2, 4, 6, 8]
```

## Modifying Lists

### Adding Elements

```python
fruits = ["apple", "banana"]

# Append to end
fruits.append("cherry")
print(fruits)  # ["apple", "banana", "cherry"]

# Insert at position
fruits.insert(1, "orange")
print(fruits)  # ["apple", "orange", "banana", "cherry"]

# Extend with another list
fruits.extend(["mango", "grape"])
```

### Removing Elements

```python
fruits = ["apple", "banana", "cherry", "banana"]

# Remove by value
fruits.remove("banana")  # Removes first occurrence

# Remove by index
del fruits[0]

# Pop (remove and return)
last_fruit = fruits.pop()  # Removes last item
first_fruit = fruits.pop(0)  # Removes first item

# Clear all
fruits.clear()
```

## List Methods

Common list operations:

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Sort
numbers.sort()
print(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]

# Reverse
numbers.reverse()
print(numbers)  # [9, 6, 5, 4, 3, 2, 1, 1]

# Count occurrences
count = numbers.count(1)  # 2

# Find index
index = numbers.index(5)

# Length
length = len(numbers)
```

## List Comprehensions

Create lists in a concise way:

```python
# Traditional way
squares = []
for i in range(10):
    squares.append(i ** 2)

# List comprehension
squares = [i ** 2 for i in range(10)]

# With condition
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
```

## Nested Lists

Lists can contain other lists:

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[0])     # [1, 2, 3]
print(matrix[0][1])  # 2
```

## Common Patterns

### Iterate over a list

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# With index
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

### Check membership

```python
fruits = ["apple", "banana", "cherry"]

if "banana" in fruits:
    print("We have bananas!")

if "mango" not in fruits:
    print("No mangos available")
```

## Exercise 1: List Operations

Create a shopping list and perform various operations:

```python
# Your code here
# 1. Create a shopping list with 5 items
# 2. Add 2 more items
# 3. Remove 1 item
# 4. Print the final list
```

## Exercise 2: List Statistics

Calculate statistics for a list of numbers:

```python
# Your code here
numbers = [23, 45, 12, 67, 34, 89, 21]
# Calculate: sum, average, min, max
```

## Exercise 3: List Filtering

Filter a list based on conditions:

```python
# Your code here
# Create a list of numbers from 1 to 20
# Create a new list with only even numbers
# Create a new list with numbers divisible by 3
```

## Key Takeaways

- Lists store ordered collections of items
- Access elements using indexing (starting at 0)
- Lists are mutable (can be changed)
- Many built-in methods for list manipulation
- List comprehensions provide concise syntax
- Lists can be nested

## Next Steps

Continue to Lesson 2.2 to learn about dictionaries and sets!
