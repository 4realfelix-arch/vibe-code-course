# Lesson 2.3: Algorithm Basics

## Overview

Algorithms are step-by-step procedures for solving problems. Understanding algorithms is essential for writing efficient code.

## What is an Algorithm?

An algorithm is a finite sequence of well-defined instructions to solve a problem or perform a task.

### Algorithm Properties

1. **Input**: Zero or more inputs
2. **Output**: At least one output
3. **Definiteness**: Clear and unambiguous steps
4. **Finiteness**: Must terminate after finite steps
5. **Effectiveness**: Steps must be doable

## Common Algorithm Patterns

### 1. Searching Algorithms

#### Linear Search
Search through each element sequentially:

```python
def linear_search(arr, target):
    """Search for target in arr using linear search"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i  # Return index if found
    return -1  # Return -1 if not found

# Example
numbers = [4, 2, 7, 1, 9, 3]
index = linear_search(numbers, 7)
print(f"Found at index: {index}")  # Output: Found at index: 2
```

#### Binary Search
Search in a sorted array by dividing in half:

```python
def binary_search(arr, target):
    """Search for target in sorted arr using binary search"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Example
numbers = [1, 2, 3, 4, 7, 9]  # Must be sorted!
index = binary_search(numbers, 7)
print(f"Found at index: {index}")  # Output: Found at index: 4
```

### 2. Sorting Algorithms

#### Bubble Sort
Repeatedly swap adjacent elements if they're in wrong order:

```python
def bubble_sort(arr):
    """Sort array using bubble sort"""
    n = len(arr)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr

# Example
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers.copy())
print(sorted_numbers)  # [11, 12, 22, 25, 34, 64, 90]
```

#### Selection Sort
Find minimum element and place it at the beginning:

```python
def selection_sort(arr):
    """Sort array using selection sort"""
    n = len(arr)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr

# Example
numbers = [64, 25, 12, 22, 11]
sorted_numbers = selection_sort(numbers.copy())
print(sorted_numbers)  # [11, 12, 22, 25, 64]
```

#### Insertion Sort
Build sorted array one item at a time:

```python
def insertion_sort(arr):
    """Sort array using insertion sort"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr

# Example
numbers = [12, 11, 13, 5, 6]
sorted_numbers = insertion_sort(numbers.copy())
print(sorted_numbers)  # [5, 6, 11, 12, 13]
```

### 3. String Algorithms

#### Palindrome Check

```python
def is_palindrome(s):
    """Check if string is a palindrome"""
    # Remove spaces and convert to lowercase
    s = s.replace(" ", "").lower()
    return s == s[::-1]

# Examples
print(is_palindrome("racecar"))  # True
print(is_palindrome("hello"))    # False
print(is_palindrome("A man a plan a canal Panama"))  # True
```

#### Anagram Check

```python
def are_anagrams(s1, s2):
    """Check if two strings are anagrams"""
    # Remove spaces and convert to lowercase
    s1 = s1.replace(" ", "").lower()
    s2 = s2.replace(" ", "").lower()
    
    return sorted(s1) == sorted(s2)

# Examples
print(are_anagrams("listen", "silent"))  # True
print(are_anagrams("hello", "world"))    # False
```

## Algorithm Design Techniques

### 1. Brute Force
Try all possible solutions:

```python
def find_max(arr):
    """Find maximum using brute force"""
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val
```

### 2. Divide and Conquer
Break problem into smaller sub-problems:

```python
def merge_sort(arr):
    """Sort using divide and conquer"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### 3. Greedy Approach
Make locally optimal choices:

```python
def coin_change_greedy(amount, coins):
    """Make change using greedy approach"""
    coins.sort(reverse=True)
    result = []
    
    for coin in coins:
        while amount >= coin:
            result.append(coin)
            amount -= coin
    
    return result

# Example
coins = [1, 5, 10, 25]
change = coin_change_greedy(67, coins)
print(change)  # [25, 25, 10, 5, 1, 1]
```

## Exercise 1: Implement Binary Search

Implement binary search from scratch:

```python
# Your code here
def binary_search(arr, target):
    # Implement binary search
    pass
```

## Exercise 2: Find Duplicates

Find duplicate elements in a list:

```python
# Your code here
def find_duplicates(arr):
    # Return list of duplicate elements
    pass
```

## Exercise 3: Two Sum Problem

Find two numbers that add up to a target:

```python
# Your code here
def two_sum(numbers, target):
    # Return indices of two numbers that add up to target
    pass

# Example
nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target))  # [0, 1] because nums[0] + nums[1] = 9
```

## Key Takeaways

- Algorithms are step-by-step problem-solving procedures
- Searching algorithms help find elements efficiently
- Sorting algorithms organize data
- Different approaches work for different problems
- Practice implementing algorithms to understand them deeply

## Next Steps

Continue to Lesson 2.4 to learn about complexity analysis!
