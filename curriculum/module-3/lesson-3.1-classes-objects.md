# Lesson 3.1: Classes and Objects

## Overview

Object-Oriented Programming (OOP) organizes code into reusable objects that combine data and behavior. This is one of the most important programming paradigms.

## What is Object-Oriented Programming?

OOP is a programming paradigm based on the concept of "objects" that contain:
- **Data** (attributes/properties)
- **Behavior** (methods/functions)

## Classes and Objects

### Classes
A class is a blueprint for creating objects:

```python
class Cat:
    """A simple Cat class"""
    pass

# Create an object (instance) of the class
my_cat = Cat()
```

### Attributes
Properties that belong to objects:

```python
class Cat:
    """Cat with attributes"""
    
    def __init__(self, name, age):
        """Constructor - initializes object"""
        self.name = name  # Instance attribute
        self.age = age
        self.energy = 100

# Create cat objects
atomic_cat = Cat("Atomic", 5)
felix = Cat("Felix", 3)

print(atomic_cat.name)  # Output: Atomic
print(felix.age)        # Output: 3
```

### Methods
Functions that belong to objects:

```python
class Cat:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.energy = 100
    
    def meow(self):
        """Cat makes a sound"""
        print(f"{self.name} says: Meow!")
    
    def play(self):
        """Cat plays and loses energy"""
        if self.energy > 10:
            self.energy -= 10
            print(f"{self.name} is playing!")
        else:
            print(f"{self.name} is too tired to play.")
    
    def sleep(self):
        """Cat sleeps and gains energy"""
        self.energy = 100
        print(f"{self.name} is sleeping... ZZZ")

# Using methods
cat = Cat("Atomic", 5)
cat.meow()   # Atomic says: Meow!
cat.play()   # Atomic is playing!
print(cat.energy)  # 90
```

## The `self` Parameter

`self` refers to the instance of the class:

```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1  # self.count refers to this instance's count
    
    def get_count(self):
        return self.count

counter1 = Counter()
counter2 = Counter()

counter1.increment()
counter1.increment()
counter2.increment()

print(counter1.get_count())  # 2
print(counter2.get_count())  # 1
```

## Class Variables vs Instance Variables

```python
class Cat:
    # Class variable (shared by all instances)
    species = "Felis catus"
    
    def __init__(self, name):
        # Instance variable (unique to each instance)
        self.name = name

cat1 = Cat("Atomic")
cat2 = Cat("Felix")

print(cat1.species)  # Felis catus
print(cat2.species)  # Felis catus
print(Cat.species)   # Felis catus

print(cat1.name)     # Atomic
print(cat2.name)     # Felix
```

## Special Methods (Magic Methods)

Methods with double underscores have special meanings:

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self):
        """String representation for print()"""
        return f"'{self.title}' by {self.author}"
    
    def __len__(self):
        """Length of the book"""
        return self.pages
    
    def __eq__(self, other):
        """Check equality"""
        return (self.title == other.title and 
                self.author == other.author)

book = Book("Python Guide", "John Doe", 350)

print(book)          # 'Python Guide' by John Doe
print(len(book))     # 350

book2 = Book("Python Guide", "John Doe", 350)
print(book == book2) # True
```

## Properties and Getters/Setters

Control access to attributes:

```python
class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance  # Protected attribute
    
    @property
    def balance(self):
        """Getter for balance"""
        return self._balance
    
    @balance.setter
    def balance(self, amount):
        """Setter for balance"""
        if amount < 0:
            print("Balance cannot be negative!")
        else:
            self._balance = amount
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited ${amount}")
    
    def withdraw(self, amount):
        if amount > self._balance:
            print("Insufficient funds!")
        else:
            self._balance -= amount
            print(f"Withdrew ${amount}")

account = BankAccount(1000)
print(account.balance)  # 1000
account.deposit(500)    # Deposited $500
account.withdraw(200)   # Withdrew $200
print(account.balance)  # 1300
```

## Class Methods and Static Methods

```python
class MathOperations:
    pi = 3.14159
    
    def __init__(self, value):
        self.value = value
    
    @classmethod
    def from_string(cls, string):
        """Alternative constructor"""
        return cls(float(string))
    
    @staticmethod
    def add(a, b):
        """Static method - no access to instance or class"""
        return a + b
    
    def square(self):
        """Instance method"""
        return self.value ** 2

# Using class method
obj = MathOperations.from_string("3.14")

# Using static method
result = MathOperations.add(5, 3)  # 8

# Using instance method
print(obj.square())  # 9.8596
```

## Exercise 1: Create a Student Class

```python
# Your code here
class Student:
    def __init__(self, name, student_id):
        # Initialize attributes
        pass
    
    def add_grade(self, grade):
        # Add grade to student's grades
        pass
    
    def get_average(self):
        # Calculate and return average grade
        pass
    
    def __str__(self):
        # Return string representation
        pass
```

## Exercise 2: Rectangle Class

```python
# Your code here
class Rectangle:
    def __init__(self, width, height):
        # Initialize dimensions
        pass
    
    def area(self):
        # Calculate area
        pass
    
    def perimeter(self):
        # Calculate perimeter
        pass
    
    def is_square(self):
        # Check if rectangle is a square
        pass
```

## Exercise 3: Shopping Cart

```python
# Your code here
class ShoppingCart:
    def __init__(self):
        # Initialize empty cart
        pass
    
    def add_item(self, item, price, quantity=1):
        # Add item to cart
        pass
    
    def remove_item(self, item):
        # Remove item from cart
        pass
    
    def get_total(self):
        # Calculate total price
        pass
    
    def __str__(self):
        # Return cart contents
        pass
```

## Key Takeaways

- Classes are blueprints for objects
- Objects combine data (attributes) and behavior (methods)
- `__init__` initializes new objects
- `self` refers to the current instance
- Special methods enable custom behavior
- Properties control attribute access
- OOP helps organize and reuse code

## Next Steps

Continue to Lesson 3.2 to learn about inheritance and polymorphism!
