# Getting Started Guide

Welcome to the Vibe Code Course! This guide will help you get started with your learning journey.

## Prerequisites

Before you begin, make sure you have:

1. **Python 3.8 or higher** installed
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **A code editor** (choose one):
   - [Visual Studio Code](https://code.visualstudio.com/) (recommended)
   - [PyCharm](https://www.jetbrains.com/pycharm/)
   - [Sublime Text](https://www.sublimetext.com/)

3. **Basic command line skills**
   - Opening terminal/command prompt
   - Navigating directories
   - Running Python scripts

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/4realfelix-arch/vibe-code-course.git
cd vibe-code-course
```

### 2. Set Up Python Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install required packages
pip install numpy pandas matplotlib scikit-learn
```

## Course Structure

The course is organized into 5 modules:

```
📚 Module 1: Foundations (Start here!)
   ├── Lesson 1.1: Introduction to Programming
   ├── Lesson 1.2: Variables and Data Types
   ├── Lesson 1.3: Control Flow and Logic
   └── Lesson 1.4: Functions and Modularity

📚 Module 2: Data Structures and Algorithms
   ├── Lesson 2.1: Arrays and Lists
   ├── Lesson 2.2: Dictionaries and Sets
   ├── Lesson 2.3: Algorithm Basics
   └── Lesson 2.4: Complexity Analysis

📚 Module 3: Object-Oriented Programming
   ├── Lesson 3.1: Classes and Objects
   ├── Lesson 3.2: Inheritance and Polymorphism
   ├── Lesson 3.3: Encapsulation and Abstraction
   └── Lesson 3.4: Design Patterns

📚 Module 4: AI and Machine Learning
   ├── Lesson 4.1: Introduction to AI
   ├── Lesson 4.2: Machine Learning Basics
   ├── Lesson 4.3: Neural Networks (Coming soon)
   └── Lesson 4.4: Deep Learning (Coming soon)

📚 Module 5: Advanced Topics (Coming soon)
   ├── Lesson 5.1: Natural Language Processing
   ├── Lesson 5.2: Computer Vision
   ├── Lesson 5.3: AI Ethics
   └── Lesson 5.4: Building AI Applications
```

## How to Use This Course

### 1. Follow the Learning Path

Start with Module 1 and progress sequentially. Each lesson builds on previous knowledge.

### 2. Read and Understand

- Read each lesson carefully
- Try to understand concepts before moving to code
- Take notes if helpful

### 3. Practice with Code

```bash
# Navigate to exercises
cd exercises

# Run example solutions
python module-1-solutions.py
```

### 4. Complete Exercises

Each lesson includes exercises. Try to solve them before looking at solutions:

```python
# Example exercise
def celsius_to_fahrenheit(celsius):
    # Your code here
    pass
```

### 5. Build Projects

Apply your knowledge with hands-on projects:

```bash
cd projects/01-calculator-app
python calculator.py
```

## Learning Tips

### 1. Type Code Yourself

Don't copy-paste! Typing helps you learn:
- Builds muscle memory
- Helps you catch errors
- Improves understanding

### 2. Experiment

Try modifying examples:
```python
# Original
print("Hello, World!")

# Try variations
print("Hello, Vibe Code!")
print("Hello, " + "Atomic Cat!")
```

### 3. Debug Errors

Errors are learning opportunities:
```python
# Error: NameError
print(message)  # message not defined

# Fix: Define the variable first
message = "Hello!"
print(message)
```

### 4. Take Breaks

- Study for 25-50 minutes
- Take 5-10 minute breaks
- Review what you learned

### 5. Practice Daily

Consistency beats intensity:
- 30 minutes daily > 3 hours once a week
- Build a learning habit
- Track your progress

## Getting Help

### Read Error Messages

```python
Traceback (most recent call last):
  File "test.py", line 5, in <module>
    result = divide(10, 0)
  File "test.py", line 2, in divide
    return a / b
ZeroDivisionError: division by zero
```

Error messages tell you:
1. What went wrong
2. Where it happened
3. What type of error

### Use Python's Help

```python
# Get help on a function
help(print)

# Get type of an object
type([1, 2, 3])

# See available methods
dir(str)
```

### Online Resources

- [Python Documentation](https://docs.python.org/3/)
- [Stack Overflow](https://stackoverflow.com/)
- [Python Subreddit](https://reddit.com/r/learnpython)

## Progress Tracking

Create a checklist to track your progress:

```markdown
## My Progress

### Module 1: Foundations
- [ ] Lesson 1.1: Introduction
- [ ] Lesson 1.2: Variables
- [ ] Lesson 1.3: Control Flow
- [ ] Lesson 1.4: Functions

### Module 2: Data Structures
- [ ] Lesson 2.1: Lists
- [ ] Lesson 2.2: Dictionaries
- [ ] Lesson 2.3: Algorithms
- [ ] Lesson 2.4: Complexity

... and so on
```

## Example Learning Session

Here's a sample 1-hour session:

**Minutes 0-5:** Review previous lesson
**Minutes 5-25:** Read new lesson
**Minutes 25-30:** Break
**Minutes 30-50:** Complete exercises
**Minutes 50-60:** Work on project or review

## Testing Your Setup

Run this test script to verify your setup:

```python
# test_setup.py
print("Python is working! ✓")

# Test basic operations
result = 2 + 2
print(f"Math works: 2 + 2 = {result} ✓")

# Test data structures
my_list = [1, 2, 3]
print(f"Lists work: {my_list} ✓")

# Test functions
def greet(name):
    return f"Hello, {name}!"

print(greet("Vibe Code") + " ✓")

print("\nSetup complete! You're ready to start learning! 🚀")
```

Save and run:
```bash
python test_setup.py
```

## Next Steps

Ready to begin? Start with:

1. Read [Module 1, Lesson 1.1](curriculum/module-1/lesson-1.1-introduction.md)
2. Complete the exercises
3. Move to Lesson 1.2

Happy learning! 🎓

---

**Remember:** Everyone learns at their own pace. Don't rush. Focus on understanding concepts deeply rather than racing through lessons.

**Questions?** Review the lesson, check the resources, or take a break and come back with fresh eyes!
