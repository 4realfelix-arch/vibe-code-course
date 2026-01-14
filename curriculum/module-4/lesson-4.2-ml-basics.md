# Lesson 4.2: Machine Learning Basics

## Overview

Machine Learning enables computers to learn from data without being explicitly programmed. This lesson covers fundamental ML concepts and algorithms.

## What is Machine Learning?

Machine Learning is a subset of AI that focuses on creating systems that learn and improve from experience.

### Types of Machine Learning

#### 1. Supervised Learning
Learning from labeled data:

```python
# Example concept
training_data = [
    ([2, 3], "cat"),      # Features → Label
    ([5, 1], "dog"),
    ([3, 4], "cat"),
]

# Model learns the pattern
model.train(training_data)

# Predict new data
prediction = model.predict([4, 2])  # → "cat" or "dog"
```

**Common Algorithms:**
- Linear Regression
- Logistic Regression
- Decision Trees
- Random Forests
- Support Vector Machines (SVM)
- Neural Networks

#### 2. Unsupervised Learning
Finding patterns in unlabeled data:

```python
# Example concept
data = [[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6]]

# Model finds clusters
clusters = model.cluster(data)
# Result: [[1,2], [1.5,1.8], [1,0.6]] and [[5,8], [8,8]]
```

**Common Algorithms:**
- K-Means Clustering
- Hierarchical Clustering
- Principal Component Analysis (PCA)
- Association Rules

#### 3. Reinforcement Learning
Learning through trial and error:

```python
# Example concept
agent = GameAgent()

for episode in range(1000):
    state = environment.reset()
    
    while not done:
        action = agent.choose_action(state)
        next_state, reward, done = environment.step(action)
        agent.learn(state, action, reward, next_state)
        state = next_state
```

## ML Workflow

### 1. Data Collection

```python
import pandas as pd

# Load data
data = pd.read_csv('data.csv')
print(data.head())
```

### 2. Data Preprocessing

```python
# Handle missing values
data = data.dropna()

# Normalize data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)
```

### 3. Split Data

```python
from sklearn.model_selection import train_test_split

X = data.drop('target', axis=1)  # Features
y = data['target']               # Labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### 4. Train Model

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
```

### 5. Evaluate Model

```python
from sklearn.metrics import accuracy_score

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.2%}")
```

## Simple Linear Regression Example

```python
import numpy as np
import matplotlib.pyplot as plt

# Generate sample data
np.random.seed(0)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

# Simple implementation
class LinearRegression:
    def __init__(self):
        self.slope = None
        self.intercept = None
    
    def fit(self, X, y):
        # Calculate slope and intercept
        n = len(X)
        x_mean = np.mean(X)
        y_mean = np.mean(y)
        
        numerator = np.sum((X - x_mean) * (y - y_mean))
        denominator = np.sum((X - x_mean) ** 2)
        
        self.slope = numerator / denominator
        self.intercept = y_mean - self.slope * x_mean
    
    def predict(self, X):
        return self.slope * X + self.intercept

# Train model
model = LinearRegression()
model.fit(X, y)

# Make predictions
X_test = np.array([[0], [2]])
predictions = model.predict(X_test)

print(f"Slope: {model.slope[0]:.2f}")
print(f"Intercept: {model.intercept[0]:.2f}")
```

## Classification Example

```python
# Simple K-Nearest Neighbors implementation
class KNN:
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None
    
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
    
    def predict(self, X):
        predictions = []
        for x in X:
            # Calculate distances to all training points
            distances = [np.sqrt(np.sum((x - x_train) ** 2)) 
                        for x_train in self.X_train]
            
            # Get k nearest neighbors
            k_indices = np.argsort(distances)[:self.k]
            k_labels = [self.y_train[i] for i in k_indices]
            
            # Vote for most common class
            prediction = max(set(k_labels), key=k_labels.count)
            predictions.append(prediction)
        
        return predictions

# Example usage
X_train = np.array([[1, 2], [2, 3], [3, 1], [6, 5], [7, 7], [8, 6]])
y_train = [0, 0, 0, 1, 1, 1]

model = KNN(k=3)
model.fit(X_train, y_train)

X_test = np.array([[3, 3], [7, 6]])
predictions = model.predict(X_test)
print(f"Predictions: {predictions}")  # [0, 1]
```

## Feature Engineering

Transforming raw data into useful features:

```python
# Example: Creating features from text
def extract_features(text):
    features = {
        'length': len(text),
        'words': len(text.split()),
        'uppercase': sum(1 for c in text if c.isupper()),
        'has_question': '?' in text,
    }
    return features

text = "How are you doing today?"
features = extract_features(text)
print(features)
# {'length': 25, 'words': 5, 'uppercase': 1, 'has_question': True}
```

## Model Evaluation Metrics

### For Classification

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# Predictions vs actual
y_true = [0, 1, 1, 0, 1, 0]
y_pred = [0, 1, 0, 0, 1, 1]

print(f"Accuracy: {accuracy_score(y_true, y_pred):.2f}")
print(f"Precision: {precision_score(y_true, y_pred):.2f}")
print(f"Recall: {recall_score(y_true, y_pred):.2f}")
print(f"F1 Score: {f1_score(y_true, y_pred):.2f}")
print(f"Confusion Matrix:\n{confusion_matrix(y_true, y_pred)}")
```

### For Regression

```python
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

y_true = [3, -0.5, 2, 7]
y_pred = [2.5, 0.0, 2, 8]

print(f"MSE: {mean_squared_error(y_true, y_pred):.2f}")
print(f"MAE: {mean_absolute_error(y_true, y_pred):.2f}")
print(f"R² Score: {r2_score(y_true, y_pred):.2f}")
```

## Cross-Validation

```python
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()

# 5-fold cross-validation
scores = cross_val_score(model, X, y, cv=5)

print(f"Scores: {scores}")
print(f"Average: {scores.mean():.2f}")
print(f"Std Dev: {scores.std():.2f}")
```

## Common ML Pitfalls

### 1. Overfitting
Model too complex, memorizes training data:

```python
# Overfitting example
from sklearn.tree import DecisionTreeClassifier

# Too deep tree overfits
overfit_model = DecisionTreeClassifier(max_depth=100)

# Regularized tree generalizes better
good_model = DecisionTreeClassifier(max_depth=5)
```

### 2. Underfitting
Model too simple, doesn't learn patterns:

```python
# Underfitting example
# Using linear model for non-linear data
```

### 3. Data Leakage
Test data influences training:

```python
# WRONG: Scale before split
scaled_data = scaler.fit_transform(data)
X_train, X_test = train_test_split(scaled_data)

# RIGHT: Split first, then scale
X_train, X_test = train_test_split(data)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)  # Use same scaler
```

## Exercise 1: Build a Predictor

```python
# Your code here
# Create a simple prediction model
# 1. Generate or load data
# 2. Split into train/test
# 3. Train a model
# 4. Evaluate accuracy
```

## Exercise 2: Feature Engineering

```python
# Your code here
def engineer_features(data):
    """
    Create new features from existing data
    Example: from age, create age_group
    """
    pass
```

## Exercise 3: Compare Models

```python
# Your code here
# Train multiple models on same data
# Compare their performance
# Which works best?
```

## Key Takeaways

- ML enables computers to learn from data
- Supervised learning uses labeled data
- Unsupervised learning finds patterns
- Feature engineering is crucial
- Always split data into train/test sets
- Evaluate models with appropriate metrics
- Avoid overfitting and underfitting
- Cross-validation provides better estimates

## Next Steps

Continue to Lesson 4.3 to learn about neural networks!
