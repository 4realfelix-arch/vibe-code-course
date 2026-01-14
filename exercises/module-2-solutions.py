"""
Exercise Solutions for Module 2
Vibe Code Curriculum for Atomic Cat AI
"""

# Lesson 2.1 Exercises

print("=== Lesson 2.1: Arrays and Lists ===\n")

# Exercise 1: List Operations
shopping_list = ["milk", "bread", "eggs", "cheese", "butter"]
print(f"Initial list: {shopping_list}")

# Add 2 more items
shopping_list.append("apples")
shopping_list.append("bananas")
print(f"After adding items: {shopping_list}")

# Remove 1 item
shopping_list.remove("bread")
print(f"After removing bread: {shopping_list}")

# Exercise 2: List Statistics
numbers = [23, 45, 12, 67, 34, 89, 21]

total_sum = sum(numbers)
average = total_sum / len(numbers)
minimum = min(numbers)
maximum = max(numbers)

print(f"\nNumbers: {numbers}")
print(f"Sum: {total_sum}")
print(f"Average: {average:.2f}")
print(f"Minimum: {minimum}")
print(f"Maximum: {maximum}")

# Exercise 3: List Filtering
all_numbers = list(range(1, 21))
even_numbers = [n for n in all_numbers if n % 2 == 0]
divisible_by_3 = [n for n in all_numbers if n % 3 == 0]

print(f"\nAll numbers: {all_numbers}")
print(f"Even numbers: {even_numbers}")
print(f"Divisible by 3: {divisible_by_3}")


# Lesson 2.2 Exercises

print("\n=== Lesson 2.2: Dictionaries and Sets ===\n")

# Exercise 1: Contact Book
contacts = {
    "Alice": "555-1234",
    "Bob": "555-5678",
    "Charlie": "555-9012"
}

print(f"Initial contacts: {contacts}")

# Look up a contact
print(f"Alice's number: {contacts['Alice']}")

# Update a contact
contacts["Bob"] = "555-0000"
print(f"After updating Bob: {contacts}")

# Delete a contact
del contacts["Charlie"]
print(f"After deleting Charlie: {contacts}")

# Exercise 2: Word Counter
sentence = "the quick brown fox jumps over the lazy dog the quick fox"
words = sentence.split()

word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

print(f"\nWord counts: {word_count}")

# Exercise 3: Unique Elements
list1 = [1, 2, 3, 4, 5, 3, 2, 1]
list2 = [4, 5, 6, 7, 8, 5, 4]

set1 = set(list1)
set2 = set(list2)

print(f"\nList 1: {list1}")
print(f"List 2: {list2}")
print(f"Unique in list1: {set1}")
print(f"Unique in list2: {set2}")
print(f"Common elements: {set1 & set2}")
print(f"Only in list1: {set1 - set2}")
print(f"Only in list2: {set2 - set1}")
