# Lesson 2.2: Dictionaries and Sets

## Overview

Dictionaries and sets are powerful data structures that help you organize and manipulate data efficiently.

## Dictionaries

Dictionaries store key-value pairs:

```python
person = {
    "name": "Atomic Cat",
    "age": 5,
    "city": "AI Town",
    "is_ai": True
}
```

### Accessing Dictionary Values

```python
print(person["name"])        # Output: Atomic Cat
print(person.get("age"))     # Output: 5
print(person.get("email", "N/A"))  # Output: N/A (default value)
```

### Modifying Dictionaries

```python
person = {"name": "Felix", "age": 25}

# Add/update
person["email"] = "felix@example.com"
person["age"] = 26

# Remove
del person["age"]
email = person.pop("email")

# Update multiple
person.update({"city": "NYC", "country": "USA"})
```

### Dictionary Methods

```python
person = {"name": "Felix", "age": 25, "city": "NYC"}

# Get all keys
keys = person.keys()

# Get all values
values = person.values()

# Get all key-value pairs
items = person.items()

# Check if key exists
if "name" in person:
    print("Name exists!")
```

### Iterating Over Dictionaries

```python
person = {"name": "Felix", "age": 25, "city": "NYC"}

# Iterate over keys
for key in person:
    print(key)

# Iterate over values
for value in person.values():
    print(value)

# Iterate over key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
```

### Nested Dictionaries

```python
students = {
    "student1": {
        "name": "Alice",
        "grades": [85, 90, 92]
    },
    "student2": {
        "name": "Bob",
        "grades": [78, 82, 88]
    }
}

print(students["student1"]["name"])  # Alice
```

## Sets

Sets are unordered collections of unique items:

```python
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 3, 4, 5}
```

### Set Operations

```python
# Add element
fruits = {"apple", "banana"}
fruits.add("cherry")

# Remove element
fruits.remove("banana")  # Raises error if not found
fruits.discard("banana")  # No error if not found

# Clear all
fruits.clear()
```

### Set Mathematics

```python
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

# Union (all elements)
union = set1 | set2  # {1, 2, 3, 4, 5, 6, 7, 8}

# Intersection (common elements)
intersection = set1 & set2  # {4, 5}

# Difference (in set1 but not set2)
difference = set1 - set2  # {1, 2, 3}

# Symmetric difference (in either but not both)
sym_diff = set1 ^ set2  # {1, 2, 3, 6, 7, 8}
```

### Set Methods

```python
set1 = {1, 2, 3}
set2 = {2, 3, 4}

# Check subset
is_subset = set1.issubset(set2)  # False

# Check superset
is_superset = set1.issuperset({1, 2})  # True

# Check disjoint (no common elements)
is_disjoint = set1.isdisjoint({5, 6})  # True
```

## Dictionary vs List vs Set

| Feature | List | Dictionary | Set |
|---------|------|------------|-----|
| Ordered | Yes | Yes (3.7+) | No |
| Indexed | Yes | By key | No |
| Duplicates | Yes | Keys: No, Values: Yes | No |
| Mutable | Yes | Yes | Yes |

## Exercise 1: Contact Book

Create a contact book using a dictionary:

```python
# Your code here
# Create a dictionary with names as keys and phone numbers as values
# Add 3 contacts
# Look up a contact
# Update a contact
# Delete a contact
```

## Exercise 2: Word Counter

Count word frequency in a sentence:

```python
# Your code here
sentence = "the quick brown fox jumps over the lazy dog the quick fox"
# Create a dictionary with word counts
```

## Exercise 3: Unique Elements

Find unique elements using sets:

```python
# Your code here
list1 = [1, 2, 3, 4, 5, 3, 2, 1]
list2 = [4, 5, 6, 7, 8, 5, 4]
# Find unique elements in both lists
# Find common elements
# Find elements only in list1
```

## Key Takeaways

- Dictionaries store key-value pairs
- Keys must be unique and immutable
- Sets store unique elements
- Sets support mathematical operations
- Both are highly efficient for lookups
- Choose based on your data structure needs

## Next Steps

Continue to Lesson 2.3 to learn about algorithm basics!
