# Lesson 3.3: Encapsulation and Abstraction

## Overview

Encapsulation and abstraction are core OOP principles that help create maintainable, secure, and easy-to-use code.

## Encapsulation

Encapsulation bundles data and methods together and restricts access to implementation details.

### Access Modifiers

Python uses naming conventions for access control:

```python
class BankAccount:
    def __init__(self, account_number, balance):
        self.account_number = account_number  # Public
        self._balance = balance              # Protected (convention)
        self.__pin = "1234"                  # Private (name mangling)
    
    def get_balance(self):
        """Public method to access private data"""
        return self._balance
    
    def __validate_pin(self, pin):
        """Private method"""
        return pin == self.__pin
    
    def withdraw(self, amount, pin):
        if self.__validate_pin(pin):
            if amount <= self._balance:
                self._balance -= amount
                return True
        return False

account = BankAccount("12345", 1000)
print(account.account_number)     # OK: Public
print(account._balance)           # Works but not recommended
# print(account.__pin)            # Error: Private attribute
print(account.get_balance())      # OK: Public method
```

### Property Decorators

Control attribute access with getters and setters:

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """Get temperature in Celsius"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Set temperature in Celsius"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """Get temperature in Fahrenheit"""
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set temperature in Fahrenheit"""
        self.celsius = (value - 32) * 5/9

temp = Temperature(25)
print(temp.celsius)      # 25
print(temp.fahrenheit)   # 77.0

temp.fahrenheit = 100
print(temp.celsius)      # 37.77...
```

### Data Validation

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) < 1:
            raise ValueError("Name cannot be empty")
        self._name = value.strip().title()

person = Person("atomic cat", 5)
print(person.name)  # Atomic Cat
# person.age = -5   # Raises ValueError
```

## Abstraction

Abstraction hides complex implementation details and shows only essential features.

### Interface Definition

```python
from abc import ABC, abstractmethod

class DataStorage(ABC):
    """Abstract interface for data storage"""
    
    @abstractmethod
    def save(self, data):
        """Save data"""
        pass
    
    @abstractmethod
    def load(self):
        """Load data"""
        pass
    
    @abstractmethod
    def delete(self):
        """Delete data"""
        pass

class FileStorage(DataStorage):
    """Concrete implementation using files"""
    
    def __init__(self, filename):
        self.filename = filename
    
    def save(self, data):
        with open(self.filename, 'w') as f:
            f.write(data)
        print(f"Data saved to {self.filename}")
    
    def load(self):
        with open(self.filename, 'r') as f:
            return f.read()
    
    def delete(self):
        import os
        os.remove(self.filename)
        print(f"Deleted {self.filename}")

class DatabaseStorage(DataStorage):
    """Concrete implementation using database"""
    
    def __init__(self, connection_string):
        self.connection = connection_string
    
    def save(self, data):
        print(f"Saving to database: {data}")
    
    def load(self):
        return "Data from database"
    
    def delete(self):
        print("Deleting from database")

# User doesn't need to know implementation details
def backup_data(storage: DataStorage, data):
    """Works with any DataStorage implementation"""
    storage.save(data)

# Usage
file_storage = FileStorage("backup.txt")
db_storage = DatabaseStorage("localhost:5432")

backup_data(file_storage, "Important data")
backup_data(db_storage, "Important data")
```

### Abstraction Layers

```python
class Database:
    """High-level database abstraction"""
    
    def __init__(self):
        self._connection = None
    
    def connect(self, host, port):
        """Simple interface - complex details hidden"""
        self._connection = self._create_connection(host, port)
        self._authenticate()
        self._initialize_pool()
    
    def _create_connection(self, host, port):
        """Hidden implementation detail"""
        print(f"Creating connection to {host}:{port}")
        return {"host": host, "port": port}
    
    def _authenticate(self):
        """Hidden implementation detail"""
        print("Authenticating...")
    
    def _initialize_pool(self):
        """Hidden implementation detail"""
        print("Initializing connection pool...")
    
    def query(self, sql):
        """Simple interface for complex operation"""
        if not self._connection:
            raise Exception("Not connected")
        return self._execute_query(sql)
    
    def _execute_query(self, sql):
        """Hidden implementation detail"""
        print(f"Executing: {sql}")
        return []

# User sees simple interface
db = Database()
db.connect("localhost", 5432)
results = db.query("SELECT * FROM users")
```

## Information Hiding

### Before (No Encapsulation)

```python
class BadBankAccount:
    def __init__(self, balance):
        self.balance = balance  # Direct access - dangerous!

account = BadBankAccount(1000)
account.balance = -5000  # Oops! Negative balance allowed
account.balance = "invalid"  # Oops! String balance allowed
```

### After (With Encapsulation)

```python
class GoodBankAccount:
    def __init__(self, balance):
        self.__balance = balance
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self.__balance

account = GoodBankAccount(1000)
# account.__balance = -5000  # Won't work!
account.withdraw(200)  # Controlled access
print(account.get_balance())  # 800
```

## Real-World Example: Email System

```python
class Email:
    """Encapsulated email class"""
    
    def __init__(self, sender, recipient, subject, body):
        self._sender = sender
        self._recipient = recipient
        self._subject = subject
        self._body = body
        self._sent = False
        self._timestamp = None
    
    @property
    def sender(self):
        return self._sender
    
    @property
    def recipient(self):
        return self._recipient
    
    @property
    def subject(self):
        return self._subject
    
    @property
    def is_sent(self):
        return self._sent
    
    def send(self):
        """Public interface - hides complex sending logic"""
        if self._sent:
            raise Exception("Email already sent")
        
        self._validate()
        self._encrypt()
        self._transmit()
        self._log()
        
        self._sent = True
        from datetime import datetime
        self._timestamp = datetime.now()
    
    def _validate(self):
        """Private: Validate email"""
        if '@' not in self._recipient:
            raise ValueError("Invalid recipient email")
    
    def _encrypt(self):
        """Private: Encrypt email"""
        print("Encrypting email...")
    
    def _transmit(self):
        """Private: Send email"""
        print(f"Sending to {self._recipient}...")
    
    def _log(self):
        """Private: Log email"""
        print("Logging email transaction...")

# Simple public interface
email = Email(
    "user@example.com",
    "friend@example.com",
    "Hello",
    "How are you?"
)
email.send()  # Complex operations hidden
```

## Exercise 1: Password Manager

```python
# Your code here
class PasswordManager:
    def __init__(self):
        # Store passwords securely (use private attributes)
        pass
    
    def add_password(self, service, password):
        # Add password with validation
        pass
    
    def get_password(self, service, master_password):
        # Retrieve password only with correct master password
        pass
    
    def _hash_password(self, password):
        # Private method to hash passwords
        pass
    
    def _verify_master_password(self, password):
        # Private method to verify master password
        pass
```

## Exercise 2: Smart Home Device

```python
# Your code here
from abc import ABC, abstractmethod

class SmartDevice(ABC):
    @abstractmethod
    def turn_on(self):
        pass
    
    @abstractmethod
    def turn_off(self):
        pass
    
    @abstractmethod
    def get_status(self):
        pass

class SmartLight(SmartDevice):
    # Implement for smart light
    # Add brightness control
    pass

class SmartThermostat(SmartDevice):
    # Implement for thermostat
    # Add temperature control
    pass
```

## Exercise 3: Book Reader

```python
# Your code here
class Book:
    def __init__(self, title, content):
        # Encapsulate book data
        # Track reading progress privately
        pass
    
    @property
    def title(self):
        # Get title
        pass
    
    @property
    def progress(self):
        # Get reading progress percentage
        pass
    
    def read_page(self):
        # Read next page and update progress
        pass
    
    def jump_to_page(self, page_number):
        # Jump to specific page with validation
        pass
```

## Key Takeaways

- Encapsulation bundles data with methods that operate on it
- Access modifiers control attribute visibility
- Properties provide controlled access to attributes
- Abstraction hides complexity and shows only essentials
- Information hiding protects data integrity
- Public interfaces should be simple and intuitive
- Private methods handle implementation details
- These principles lead to more maintainable code

## Next Steps

Continue to Lesson 3.4 to learn about design patterns!
