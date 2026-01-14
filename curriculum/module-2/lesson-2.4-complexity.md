# Lesson 2.4: Complexity Analysis

## Overview

Understanding algorithm efficiency is crucial for writing performant code. This lesson covers Big O notation and complexity analysis.

## What is Complexity Analysis?

Complexity analysis measures how an algorithm's resource usage grows with input size.

### Two Types of Complexity

1. **Time Complexity**: How execution time grows
2. **Space Complexity**: How memory usage grows

## Big O Notation

Big O describes the upper bound of growth rate.

### Common Time Complexities

#### O(1) - Constant Time
Execution time doesn't depend on input size:

```python
def get_first_element(arr):
    """Always takes same time regardless of array size"""
    return arr[0]  # O(1)
```

#### O(log n) - Logarithmic Time
Execution time grows logarithmically:

```python
def binary_search(arr, target):
    """Divides problem in half each time"""
    left, right = 0, len(arr) - 1
    
    while left <= right:  # O(log n)
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

#### O(n) - Linear Time
Execution time grows linearly with input:

```python
def find_max(arr):
    """Must check every element"""
    max_val = arr[0]
    for num in arr:  # O(n)
        if num > max_val:
            max_val = num
    return max_val
```

#### O(n log n) - Linearithmic Time
Efficient sorting algorithms:

```python
def merge_sort(arr):
    """Divide (log n) and merge (n) operations"""
    # Merge sort is O(n log n)
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)
```

#### O(n²) - Quadratic Time
Nested loops over input:

```python
def bubble_sort(arr):
    """Nested loops through array"""
    n = len(arr)
    for i in range(n):  # O(n)
        for j in range(n - i - 1):  # O(n)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
# Total: O(n²)
```

#### O(2ⁿ) - Exponential Time
Doubles with each additional input:

```python
def fibonacci_recursive(n):
    """Each call makes two more calls"""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)
# O(2ⁿ) - very slow!
```

#### O(n!) - Factorial Time
Generates all permutations:

```python
def generate_permutations(arr):
    """Generate all possible arrangements"""
    # O(n!) - extremely slow!
    if len(arr) <= 1:
        return [arr]
    
    result = []
    for i in range(len(arr)):
        rest = arr[:i] + arr[i+1:]
        for perm in generate_permutations(rest):
            result.append([arr[i]] + perm)
    
    return result
```

## Complexity Chart

From fastest to slowest:

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)
```

### Growth Comparison

For n = 100:
- O(1): 1 operation
- O(log n): ~7 operations
- O(n): 100 operations
- O(n log n): ~700 operations
- O(n²): 10,000 operations
- O(2ⁿ): ~1.3 × 10³⁰ operations
- O(n!): astronomical!

## Space Complexity

Memory usage of algorithms:

### O(1) - Constant Space

```python
def sum_array(arr):
    """Only uses one variable"""
    total = 0  # O(1) space
    for num in arr:
        total += num
    return total
```

### O(n) - Linear Space

```python
def double_array(arr):
    """Creates new array of same size"""
    result = []  # O(n) space
    for num in arr:
        result.append(num * 2)
    return result
```

### O(n²) - Quadratic Space

```python
def create_matrix(n):
    """Creates n×n matrix"""
    matrix = []  # O(n²) space
    for i in range(n):
        row = [0] * n
        matrix.append(row)
    return matrix
```

## Analyzing Complex Code

### Multiple Steps

```python
def process_data(arr):
    # Step 1: O(n)
    for item in arr:
        print(item)
    
    # Step 2: O(n²)
    for i in arr:
        for j in arr:
            print(i, j)
    
    # Total: O(n) + O(n²) = O(n²)
    # We keep the dominant term
```

### Nested Loops with Different Inputs

```python
def print_pairs(arr1, arr2):
    for i in arr1:      # O(n)
        for j in arr2:  # O(m)
            print(i, j)
    # Total: O(n × m)
```

## Best, Average, and Worst Case

Algorithms can have different complexities depending on input:

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# Best case: O(1) - target is first element
# Average case: O(n/2) = O(n)
# Worst case: O(n) - target is last or not present
```

## Optimization Strategies

### 1. Use Better Data Structures

```python
# Slow: O(n) lookup
def find_in_list(lst, target):
    return target in lst  # O(n)

# Fast: O(1) lookup
def find_in_set(st, target):
    return target in st  # O(1)
```

### 2. Avoid Nested Loops

```python
# Slow: O(n²)
def has_duplicate_slow(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False

# Fast: O(n)
def has_duplicate_fast(arr):
    seen = set()
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False
```

### 3. Use Caching/Memoization

```python
# Slow: O(2ⁿ)
def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n-1) + fib_slow(n-2)

# Fast: O(n)
def fib_fast(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_fast(n-1, memo) + fib_fast(n-2, memo)
    return memo[n]
```

## Exercise 1: Analyze Complexity

Determine the time complexity of these functions:

```python
# Your analysis here

def func1(arr):
    return arr[0]

def func2(arr):
    return sum(arr)

def func3(arr):
    for i in arr:
        for j in arr:
            print(i * j)

def func4(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    return func4(arr[:mid]) + func4(arr[mid:])
```

## Exercise 2: Optimize This Code

Optimize this function to be O(n) instead of O(n²):

```python
# Your code here
def find_common_elements_slow(list1, list2):
    """O(n²) - can you make it O(n)?"""
    common = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                common.append(item1)
    return common
```

## Exercise 3: Space-Time Tradeoff

Compare these two approaches:

```python
# Approach 1: Less space, more time
def is_unique_chars_1(string):
    # Your analysis
    for i in range(len(string)):
        for j in range(i + 1, len(string)):
            if string[i] == string[j]:
                return False
    return True

# Approach 2: More space, less time
def is_unique_chars_2(string):
    # Your analysis
    char_set = set()
    for char in string:
        if char in char_set:
            return False
        char_set.add(char)
    return True
```

## Key Takeaways

- Big O notation describes algorithm efficiency
- Time complexity measures execution time growth
- Space complexity measures memory usage growth
- Choose appropriate complexity for your use case
- Sometimes we trade space for time (or vice versa)
- Understanding complexity helps write efficient code

## Module 2 Complete!

Congratulations! You've completed Module 2. You now understand:
- Lists and arrays
- Dictionaries and sets
- Common algorithms
- Complexity analysis

Continue to Module 3 to learn about object-oriented programming!
