# Lesson 4.1: Introduction to AI

## Overview

Artificial Intelligence (AI) is revolutionizing how we interact with technology. This lesson introduces core AI concepts and their applications.

## What is Artificial Intelligence?

AI is the simulation of human intelligence by machines. It enables computers to:
- Learn from experience
- Adapt to new inputs
- Perform human-like tasks

### Types of AI

1. **Narrow AI (Weak AI)**
   - Designed for specific tasks
   - Examples: Siri, recommendation systems, chess computers
   
2. **General AI (Strong AI)**
   - Human-level intelligence across all tasks
   - Currently theoretical
   
3. **Super AI**
   - Exceeds human intelligence
   - Hypothetical future possibility

## Key AI Concepts

### 1. Machine Learning (ML)
Systems that learn from data without explicit programming:

```python
# Conceptual example
training_data = load_training_data()
model = train_model(training_data)
prediction = model.predict(new_data)
```

### 2. Neural Networks
Computing systems inspired by biological neural networks:

```
Input Layer → Hidden Layers → Output Layer
```

### 3. Deep Learning
Neural networks with many layers:

```python
# Simplified concept
layers = [
    InputLayer(784),
    HiddenLayer(128),
    HiddenLayer(64),
    OutputLayer(10)
]
```

## AI Applications

### 1. Computer Vision
- Image recognition
- Object detection
- Facial recognition

### 2. Natural Language Processing (NLP)
- Language translation
- Sentiment analysis
- Chatbots

### 3. Recommendation Systems
- Netflix recommendations
- Spotify playlists
- Amazon product suggestions

### 4. Autonomous Systems
- Self-driving cars
- Drones
- Robots

## AI vs Traditional Programming

| Traditional Programming | AI/ML |
|------------------------|-------|
| Rules → Answers | Data → Patterns |
| Explicit instructions | Learn from examples |
| Predictable | Probabilistic |

## Basic AI Workflow

1. **Data Collection**: Gather relevant data
2. **Data Preparation**: Clean and format data
3. **Model Selection**: Choose appropriate algorithm
4. **Training**: Teach the model with data
5. **Evaluation**: Test model performance
6. **Deployment**: Use model in production
7. **Monitoring**: Track and improve

## Python for AI

Python is the dominant language for AI:

```python
# Popular AI libraries
import numpy as np           # Numerical computing
import pandas as pd          # Data manipulation
import matplotlib.pyplot as plt  # Visualization
import sklearn              # Machine learning
import tensorflow as tf     # Deep learning
import torch                # Deep learning
```

## Your First AI Program

A simple prediction model concept:

```python
def simple_predictor(data):
    """
    A basic pattern recognition example
    """
    # Calculate average
    average = sum(data) / len(data)
    
    # Predict next value based on trend
    trend = data[-1] - data[0]
    prediction = data[-1] + (trend / len(data))
    
    return prediction

# Usage
sales_data = [100, 120, 135, 150, 170]
next_month = simple_predictor(sales_data)
print(f"Predicted sales: {next_month}")
```

## AI Ethics Considerations

Important ethical principles:

1. **Fairness**: Avoid bias in AI systems
2. **Transparency**: Make AI decisions explainable
3. **Privacy**: Protect user data
4. **Accountability**: Take responsibility for AI actions
5. **Safety**: Ensure AI systems are secure

## Exercise 1: AI Identification

Identify which of these are AI applications:

```python
# Your answers here
applications = [
    "Calculator app",
    "Spam email filter",
    "Digital thermometer",
    "Voice assistant",
    "GPS navigation",
    "Netflix recommendations"
]
# Which ones use AI?
```

## Exercise 2: Simple Pattern Detector

Create a function that detects if a list follows an arithmetic pattern:

```python
# Your code here
def detect_pattern(numbers):
    """
    Detect if numbers follow an arithmetic sequence
    Returns the common difference or None
    """
    pass

# Test
print(detect_pattern([2, 4, 6, 8]))  # Should return 2
print(detect_pattern([1, 4, 7, 10])) # Should return 3
print(detect_pattern([1, 2, 4, 8]))  # Should return None
```

## Exercise 3: Basic Classifier

Create a simple rule-based classifier:

```python
# Your code here
def classify_temperature(temp):
    """
    Classify temperature as: freezing, cold, mild, warm, hot
    """
    pass

# Test
print(classify_temperature(25))  # cold
print(classify_temperature(60))  # mild
print(classify_temperature(90))  # hot
```

## Key Takeaways

- AI simulates human intelligence in machines
- Machine learning enables systems to learn from data
- Neural networks are inspired by the human brain
- AI has many real-world applications
- Python is the leading language for AI development
- AI ethics is crucial for responsible development

## Next Steps

Continue to Lesson 4.2 to learn about machine learning basics!
