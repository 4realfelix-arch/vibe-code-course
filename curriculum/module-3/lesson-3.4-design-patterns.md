# Lesson 3.4: Design Patterns

## Overview

Design patterns are reusable solutions to common programming problems. They represent best practices developed by experienced programmers.

## What are Design Patterns?

Design patterns are templates for solving recurring design problems in software development.

### Categories of Patterns

1. **Creational**: Object creation mechanisms
2. **Structural**: Object composition and relationships
3. **Behavioral**: Object communication and responsibility

## Creational Patterns

### 1. Singleton Pattern

Ensure a class has only one instance:

```python
class DatabaseConnection:
    """Singleton: Only one database connection"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.connection = "Connected to database"
        print("Database connection created")
    
    def query(self, sql):
        return f"Executing: {sql}"

# Both variables reference the same instance
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(db1 is db2)  # True - same object
```

### 2. Factory Pattern

Create objects without specifying exact class:

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    """Factory to create animals"""
    
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

# Using factory
factory = AnimalFactory()
dog = factory.create_animal("dog")
cat = factory.create_animal("cat")

print(dog.speak())  # Woof!
print(cat.speak())  # Meow!
```

### 3. Builder Pattern

Construct complex objects step by step:

```python
class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False
    
    def __str__(self):
        toppings = []
        if self.cheese:
            toppings.append("cheese")
        if self.pepperoni:
            toppings.append("pepperoni")
        if self.mushrooms:
            toppings.append("mushrooms")
        return f"{self.size} pizza with {', '.join(toppings)}"

class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()
    
    def set_size(self, size):
        self.pizza.size = size
        return self
    
    def add_cheese(self):
        self.pizza.cheese = True
        return self
    
    def add_pepperoni(self):
        self.pizza.pepperoni = True
        return self
    
    def add_mushrooms(self):
        self.pizza.mushrooms = True
        return self
    
    def build(self):
        return self.pizza

# Build pizza step by step
pizza = (PizzaBuilder()
         .set_size("large")
         .add_cheese()
         .add_pepperoni()
         .add_mushrooms()
         .build())

print(pizza)  # large pizza with cheese, pepperoni, mushrooms
```

## Structural Patterns

### 1. Adapter Pattern

Make incompatible interfaces work together:

```python
class EuropeanSocket:
    def voltage(self):
        return 230
    
    def socket_type(self):
        return "Type C"

class USASocket:
    def voltage(self):
        return 110
    
    def socket_type(self):
        return "Type A"

class SocketAdapter:
    """Adapter for using European devices in USA"""
    
    def __init__(self, european_socket):
        self.european_socket = european_socket
    
    def voltage(self):
        # Convert voltage
        return 110
    
    def socket_type(self):
        return "Type A (adapted from Type C)"

# Using adapter
eu_socket = EuropeanSocket()
adapter = SocketAdapter(eu_socket)
print(f"Adapted voltage: {adapter.voltage()}V")
```

### 2. Decorator Pattern

Add behavior to objects dynamically:

```python
class Coffee:
    def cost(self):
        return 5
    
    def description(self):
        return "Coffee"

class MilkDecorator:
    def __init__(self, coffee):
        self.coffee = coffee
    
    def cost(self):
        return self.coffee.cost() + 1
    
    def description(self):
        return self.coffee.description() + ", Milk"

class SugarDecorator:
    def __init__(self, coffee):
        self.coffee = coffee
    
    def cost(self):
        return self.coffee.cost() + 0.5
    
    def description(self):
        return self.coffee.description() + ", Sugar"

# Build customized coffee
coffee = Coffee()
coffee = MilkDecorator(coffee)
coffee = SugarDecorator(coffee)

print(coffee.description())  # Coffee, Milk, Sugar
print(f"Cost: ${coffee.cost()}")  # Cost: $6.5
```

### 3. Facade Pattern

Provide simplified interface to complex system:

```python
class CPU:
    def freeze(self):
        print("CPU: Freezing...")
    
    def execute(self):
        print("CPU: Executing...")

class Memory:
    def load(self):
        print("Memory: Loading...")

class HardDrive:
    def read(self):
        print("HardDrive: Reading...")

class ComputerFacade:
    """Simplified interface to start computer"""
    
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
    
    def start(self):
        """Simple method hides complex startup"""
        print("Starting computer...")
        self.cpu.freeze()
        self.memory.load()
        self.hard_drive.read()
        self.cpu.execute()
        print("Computer started!")

# Simple interface for user
computer = ComputerFacade()
computer.start()  # Hides all complexity
```

## Behavioral Patterns

### 1. Observer Pattern

Objects notify observers of state changes:

```python
class Subject:
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)
    
    def set_state(self, state):
        self._state = state
        self.notify()

class Observer:
    def __init__(self, name):
        self.name = name
    
    def update(self, state):
        print(f"{self.name} received update: {state}")

# Using observer pattern
subject = Subject()

observer1 = Observer("Observer 1")
observer2 = Observer("Observer 2")

subject.attach(observer1)
subject.attach(observer2)

subject.set_state("New state!")
# Output:
# Observer 1 received update: New state!
# Observer 2 received update: New state!
```

### 2. Strategy Pattern

Define family of algorithms and make them interchangeable:

```python
class PaymentStrategy:
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying ${amount} with credit card")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying ${amount} with PayPal")

class BitcoinPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paying ${amount} with Bitcoin")

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item, price):
        self.items.append({"item": item, "price": price})
    
    def set_payment_strategy(self, strategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        total = sum(item["price"] for item in self.items)
        self.payment_strategy.pay(total)

# Using strategy
cart = ShoppingCart()
cart.add_item("Book", 20)
cart.add_item("Pen", 5)

# Choose payment strategy at runtime
cart.set_payment_strategy(CreditCardPayment())
cart.checkout()  # Paying $25 with credit card

cart.set_payment_strategy(PayPalPayment())
cart.checkout()  # Paying $25 with PayPal
```

### 3. Command Pattern

Encapsulate requests as objects:

```python
class Command:
    def execute(self):
        pass
    
    def undo(self):
        pass

class Light:
    def on(self):
        print("Light is ON")
    
    def off(self):
        print("Light is OFF")

class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.on()
    
    def undo(self):
        self.light.off()

class RemoteControl:
    def __init__(self):
        self.command = None
    
    def set_command(self, command):
        self.command = command
    
    def press_button(self):
        self.command.execute()
    
    def press_undo(self):
        self.command.undo()

# Using command pattern
light = Light()
light_on = LightOnCommand(light)

remote = RemoteControl()
remote.set_command(light_on)
remote.press_button()  # Light is ON
remote.press_undo()    # Light is OFF
```

## Exercise 1: Implement Factory Pattern

```python
# Your code here
class Shape:
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        return "Drawing Circle"

class Square(Shape):
    def draw(self):
        return "Drawing Square"

class ShapeFactory:
    # Implement factory to create shapes
    pass
```

## Exercise 2: Implement Observer Pattern

```python
# Your code here
class NewsAgency:
    # Implement as subject that notifies subscribers
    pass

class Subscriber:
    # Implement as observer that receives updates
    pass

# Create news agency and subscribers
# Test notification system
```

## Exercise 3: Implement Strategy Pattern

```python
# Your code here
class SortStrategy:
    def sort(self, data):
        pass

class BubbleSort(SortStrategy):
    # Implement bubble sort
    pass

class QuickSort(SortStrategy):
    # Implement quick sort (or simulate)
    pass

class Sorter:
    # Use strategy pattern to sort with different algorithms
    pass
```

## Key Takeaways

- Design patterns are proven solutions to common problems
- Creational patterns handle object creation
- Structural patterns organize object relationships
- Behavioral patterns manage object interactions
- Patterns improve code reusability and maintainability
- Understanding patterns helps communicate design ideas
- Use patterns appropriately - don't force them

## Module 3 Complete!

Congratulations! You've completed Module 3. You now understand:
- Classes and objects
- Inheritance and polymorphism
- Encapsulation and abstraction
- Design patterns

Continue to Module 4 to dive into AI and machine learning!
