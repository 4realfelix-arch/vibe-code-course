# Lesson 3.2: Inheritance and Polymorphism

## Overview

Inheritance allows classes to inherit attributes and methods from other classes. Polymorphism enables objects of different types to be treated uniformly.

## Inheritance

Inheritance creates a relationship between classes where a child class inherits from a parent class.

### Basic Inheritance

```python
class Animal:
    """Parent class"""
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def make_sound(self):
        print(f"{self.name} makes a sound")
    
    def sleep(self):
        print(f"{self.name} is sleeping")

class Dog(Animal):
    """Child class inheriting from Animal"""
    def make_sound(self):
        print(f"{self.name} barks: Woof!")

class Cat(Animal):
    """Child class inheriting from Animal"""
    def make_sound(self):
        print(f"{self.name} meows: Meow!")

# Using inherited classes
dog = Dog("Rex", 5)
cat = Cat("Whiskers", 3)

dog.make_sound()  # Rex barks: Woof!
cat.make_sound()  # Whiskers meows: Meow!
dog.sleep()       # Rex is sleeping (inherited from Animal)
```

### The `super()` Function

Call parent class methods:

```python
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def info(self):
        return f"{self.brand} {self.model}"

class Car(Vehicle):
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)  # Call parent constructor
        self.doors = doors
    
    def info(self):
        parent_info = super().info()  # Call parent method
        return f"{parent_info} with {self.doors} doors"

car = Car("Toyota", "Camry", 4)
print(car.info())  # Toyota Camry with 4 doors
```

### Multiple Inheritance

Inherit from multiple parent classes:

```python
class Flyer:
    def fly(self):
        print("Flying through the air!")

class Swimmer:
    def swim(self):
        print("Swimming in water!")

class Duck(Flyer, Swimmer):
    def __init__(self, name):
        self.name = name
    
    def quack(self):
        print(f"{self.name} says: Quack!")

duck = Duck("Donald")
duck.fly()    # Flying through the air!
duck.swim()   # Swimming in water!
duck.quack()  # Donald says: Quack!
```

## Polymorphism

Polymorphism means "many forms" - different classes can implement the same method differently.

### Method Overriding

```python
class Shape:
    def area(self):
        pass
    
    def perimeter(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# Polymorphism in action
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Circle(3)
]

for shape in shapes:
    print(f"Area: {shape.area():.2f}")
```

### Duck Typing

"If it walks like a duck and quacks like a duck, it's a duck"

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Robot:
    def speak(self):
        return "Beep boop!"

def make_it_speak(obj):
    """Works with any object that has a speak() method"""
    print(obj.speak())

# All different types, but same interface
animals = [Dog(), Cat(), Robot()]

for animal in animals:
    make_it_speak(animal)
# Output:
# Woof!
# Meow!
# Beep boop!
```

## Abstract Base Classes

Define interfaces that child classes must implement:

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    """Abstract base class"""
    
    @abstractmethod
    def pay(self, amount):
        """All payment methods must implement this"""
        pass

class CreditCard(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number
    
    def pay(self, amount):
        print(f"Paying ${amount} with credit card {self.card_number}")

class PayPal(PaymentMethod):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        print(f"Paying ${amount} via PayPal ({self.email})")

# Cannot instantiate abstract class
# payment = PaymentMethod()  # Error!

# Must implement abstract methods
cc = CreditCard("1234-5678")
pp = PayPal("user@example.com")

cc.pay(100)  # Paying $100 with credit card 1234-5678
pp.pay(50)   # Paying $50 via PayPal (user@example.com)
```

## Composition vs Inheritance

Sometimes composition is better than inheritance:

```python
# Using Inheritance (is-a relationship)
class Engine:
    def start(self):
        print("Engine starting...")

class Car(Engine):  # A car IS-A engine? Not quite right!
    pass

# Using Composition (has-a relationship)
class Engine:
    def start(self):
        print("Engine starting...")

class Car:
    def __init__(self):
        self.engine = Engine()  # A car HAS-A engine!
    
    def start(self):
        self.engine.start()
        print("Car is ready to drive!")

car = Car()
car.start()
# Engine starting...
# Car is ready to drive!
```

## Method Resolution Order (MRO)

Python's order for looking up methods:

```python
class A:
    def method(self):
        print("A method")

class B(A):
    def method(self):
        print("B method")

class C(A):
    def method(self):
        print("C method")

class D(B, C):
    pass

d = D()
d.method()  # Output: B method

# Check MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

## Exercise 1: Employee Hierarchy

```python
# Your code here
class Employee:
    def __init__(self, name, employee_id, salary):
        # Initialize base employee
        pass
    
    def get_info(self):
        # Return employee information
        pass

class Manager(Employee):
    def __init__(self, name, employee_id, salary, department):
        # Initialize manager with department
        pass
    
    def get_info(self):
        # Return manager information including department
        pass

class Developer(Employee):
    def __init__(self, name, employee_id, salary, programming_language):
        # Initialize developer
        pass
    
    def get_info(self):
        # Return developer information
        pass
```

## Exercise 2: Shape Calculator

```python
# Your code here
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass

class Square(Shape):
    # Implement for square
    pass

class Triangle(Shape):
    # Implement for triangle
    pass

# Test with polymorphism
shapes = [Square(5), Triangle(3, 4, 5)]
for shape in shapes:
    print(f"Area: {shape.area()}, Perimeter: {shape.perimeter()}")
```

## Exercise 3: Library System

```python
# Your code here
class LibraryItem:
    def __init__(self, title, item_id):
        # Base class for library items
        pass
    
    def checkout(self):
        pass
    
    def return_item(self):
        pass

class Book(LibraryItem):
    def __init__(self, title, item_id, author, pages):
        # Book specific attributes
        pass

class DVD(LibraryItem):
    def __init__(self, title, item_id, director, duration):
        # DVD specific attributes
        pass
```

## Key Takeaways

- Inheritance creates parent-child class relationships
- Child classes inherit attributes and methods from parents
- `super()` calls parent class methods
- Polymorphism allows different classes to implement same interface
- Method overriding changes inherited behavior
- Abstract base classes define required interfaces
- Composition is sometimes better than inheritance
- MRO determines method lookup order

## Next Steps

Continue to Lesson 3.3 to learn about encapsulation and abstraction!
