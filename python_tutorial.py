# ============================================================
# Python Fundamentals Tutorial
# ============================================================
# Run any section by copying it into a Python REPL or script.
# Python 3.8+ is assumed throughout.


# ------------------------------------------------------------
# 1. VARIABLES & DATA TYPES
# ------------------------------------------------------------

# Python is dynamically typed — no need to declare types.
name = "Alice"          # str
age = 30                # int
height = 5.7            # float
is_student = True       # bool
nothing = None          # NoneType

print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>

# Type conversion
print(int("42"))        # 42
print(float(7))         # 7.0
print(str(100))         # '100'
print(bool(0))          # False  (0, "", [], None are all falsy)


# ------------------------------------------------------------
# 2. STRINGS
# ------------------------------------------------------------

greeting = "Hello, World!"

# Indexing & slicing (0-based, end index is exclusive)
print(greeting[0])      # H
print(greeting[-1])     # !
print(greeting[0:5])    # Hello
print(greeting[::-1])   # !dlroW ,olleH  (reversed)

# Common string methods
print(greeting.upper())             # HELLO, WORLD!
print(greeting.lower())             # hello, world!
print(greeting.replace("World", "Python"))  # Hello, Python!
print("  spaces  ".strip())         # 'spaces'
print(",".join(["a", "b", "c"]))    # a,b,c
print("a,b,c".split(","))           # ['a', 'b', 'c']

# f-strings (formatted string literals) — the modern way
language = "Python"
version = 3.12
print(f"{language} {version} is great!")   # Python 3.12 is great!
print(f"{2 + 2}")                           # 4
print(f"{name!r}")                          # 'Alice'  (repr)


# ------------------------------------------------------------
# 3. NUMBERS & OPERATORS
# ------------------------------------------------------------

# Arithmetic
print(10 + 3)    # 13
print(10 - 3)    # 7
print(10 * 3)    # 30
print(10 / 3)    # 3.3333...  (always float)
print(10 // 3)   # 3          (floor division)
print(10 % 3)    # 1          (modulo / remainder)
print(10 ** 3)   # 1000       (exponentiation)

# Comparison  → always returns bool
print(5 > 3)     # True
print(5 == 5)    # True
print(5 != 4)    # True

# Logical
print(True and False)   # False
print(True or False)    # True
print(not True)         # False

# Augmented assignment
x = 10
x += 5   # x = 15
x *= 2   # x = 30


# ------------------------------------------------------------
# 4. LISTS
# ------------------------------------------------------------

fruits = ["apple", "banana", "cherry"]

# Access
print(fruits[0])        # apple
print(fruits[-1])       # cherry

# Modify
fruits.append("date")           # add to end
fruits.insert(1, "avocado")     # insert at index
fruits.remove("banana")         # remove first match
popped = fruits.pop()           # remove & return last item
print(fruits)

# Useful operations
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(len(numbers))     # 8
print(sorted(numbers))  # sorted copy
print(min(numbers), max(numbers), sum(numbers))

# List slicing
print(numbers[2:5])     # [4, 1, 5]
print(numbers[::2])     # every other element

# List comprehension — concise way to build lists
squares = [x**2 for x in range(1, 6)]      # [1, 4, 9, 16, 25]
evens   = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]


# ------------------------------------------------------------
# 5. TUPLES
# ------------------------------------------------------------

# Like lists but immutable (cannot be changed after creation).
point = (3, 7)
x, y = point        # unpacking
print(x, y)         # 3 7

rgb = (255, 128, 0)
print(rgb[0])       # 255  (indexing works, but rgb[0] = 1 would raise TypeError)

# Single-element tuple needs a trailing comma
single = (42,)


# ------------------------------------------------------------
# 6. DICTIONARIES
# ------------------------------------------------------------

person = {
    "name": "Bob",
    "age": 25,
    "city": "Berlin",
}

# Access
print(person["name"])           # Bob
print(person.get("country", "Unknown"))  # Unknown  (safe lookup with default)

# Modify
person["age"] = 26
person["email"] = "bob@example.com"
del person["city"]

# Iterate
for key, value in person.items():
    print(f"{key}: {value}")

# Dict comprehension
squares_dict = {n: n**2 for n in range(1, 6)}  # {1:1, 2:4, 3:9, 4:16, 5:25}

# Useful methods
print(list(person.keys()))
print(list(person.values()))


# ------------------------------------------------------------
# 7. SETS
# ------------------------------------------------------------

# Unordered, unique elements.
colors = {"red", "green", "blue", "red"}  # duplicate removed
print(colors)                # {'red', 'green', 'blue'}

colors.add("yellow")
colors.discard("green")      # no error if missing (vs .remove())

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a & b)    # {3, 4}       intersection
print(a | b)    # {1,2,3,4,5,6} union
print(a - b)    # {1, 2}       difference


# ------------------------------------------------------------
# 8. CONTROL FLOW
# ------------------------------------------------------------

# if / elif / else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
print(grade)    # B

# Ternary (inline if)
label = "pass" if score >= 60 else "fail"

# for loop — iterates over any iterable
for fruit in ["apple", "banana", "cherry"]:
    print(fruit)

for i in range(5):          # 0 1 2 3 4
    print(i, end=" ")

for i, fruit in enumerate(["apple", "banana"]):
    print(i, fruit)         # 0 apple  /  1 banana

# while loop
count = 0
while count < 3:
    print(count)
    count += 1

# break / continue
for n in range(10):
    if n == 5:
        break       # stop loop
    if n % 2 == 0:
        continue    # skip to next iteration
    print(n)        # 1 3


# ------------------------------------------------------------
# 9. FUNCTIONS
# ------------------------------------------------------------

# Basic function
def greet(name):
    return f"Hello, {name}!"

print(greet("Charlie"))     # Hello, Charlie!

# Default arguments
def power(base, exponent=2):
    return base ** exponent

print(power(3))     # 9
print(power(3, 3))  # 27

# *args — variable positional arguments (tuple)
def add(*numbers):
    return sum(numbers)

print(add(1, 2, 3, 4))   # 10

# **kwargs — variable keyword arguments (dict)
def describe(**info):
    for k, v in info.items():
        print(f"  {k} = {v}")

describe(name="Dana", age=22, city="Tokyo")

# Type hints (documentation, not enforcement)
def multiply(a: int, b: int) -> int:
    return a * b

# Lambda — anonymous one-liner function
double = lambda x: x * 2
print(double(5))    # 10

# Built-in higher-order functions
nums = [1, 2, 3, 4, 5]
print(list(map(lambda x: x**2, nums)))          # [1, 4, 9, 16, 25]
print(list(filter(lambda x: x > 2, nums)))      # [3, 4, 5]


# ------------------------------------------------------------
# 10. CLASSES & OBJECTS
# ------------------------------------------------------------

class Animal:
    # Class-level attribute (shared by all instances)
    kingdom = "Animalia"

    def __init__(self, name, sound):    # constructor
        self.name = name                # instance attribute
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}!"

    def __repr__(self):                 # official string representation
        return f"Animal({self.name!r})"


class Dog(Animal):                      # inheritance
    def __init__(self, name):
        super().__init__(name, "Woof")  # call parent constructor

    def fetch(self, item):
        return f"{self.name} fetches the {item}!"


rex = Dog("Rex")
print(rex.speak())          # Rex says Woof!
print(rex.fetch("ball"))    # Rex fetches the ball!
print(rex.kingdom)          # Animalia
print(isinstance(rex, Animal))  # True


# ------------------------------------------------------------
# 11. ERROR HANDLING
# ------------------------------------------------------------

# try / except / else / finally
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except TypeError as e:
        return f"Type error: {e}"
    else:
        # runs only if no exception occurred
        return result
    finally:
        pass    # always runs — good for cleanup

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # Cannot divide by zero

# Raise your own exceptions
def set_age(age):
    if age < 0:
        raise ValueError(f"Age cannot be negative: {age}")
    return age


# ------------------------------------------------------------
# 12. FILE I/O
# ------------------------------------------------------------

# Writing a file
with open("demo.txt", "w") as f:        # 'w' = write, creates/overwrites
    f.write("Line 1\n")
    f.write("Line 2\n")

# Reading a file
with open("demo.txt", "r") as f:        # 'r' = read (default)
    content = f.read()
    print(content)

# Reading line by line (memory-efficient for large files)
with open("demo.txt") as f:
    for line in f:
        print(line.strip())

# Appending
with open("demo.txt", "a") as f:        # 'a' = append
    f.write("Line 3\n")

# The 'with' statement automatically closes the file, even on errors.


# ------------------------------------------------------------
# 13. MODULES & IMPORTS
# ------------------------------------------------------------

import os
import math
from datetime import datetime, date
from collections import Counter, defaultdict

print(math.pi)              # 3.14159...
print(math.sqrt(16))        # 4.0
print(os.getcwd())          # current working directory
print(datetime.now())       # current date & time

# Counter — count occurrences
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(words)
print(counts)                       # Counter({'apple': 3, 'banana': 2, ...})
print(counts.most_common(2))        # [('apple', 3), ('banana', 2)]

# defaultdict — dict with a default factory
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
dd["vegs"].append("carrot")
print(dict(dd))


# ------------------------------------------------------------
# 14. COMPREHENSIONS SUMMARY
# ------------------------------------------------------------

# List comprehension
squares = [x**2 for x in range(1, 6)]

# Dict comprehension
word_lengths = {word: len(word) for word in ["cat", "elephant", "ox"]}

# Set comprehension
unique_lengths = {len(word) for word in ["cat", "elephant", "ox"]}

# Generator expression (lazy, memory-efficient — no brackets)
total = sum(x**2 for x in range(1_000_000))


# ------------------------------------------------------------
# 15. USEFUL BUILT-INS CHEAT SHEET
# ------------------------------------------------------------
#
#  len(x)          — number of items
#  range(n)        — 0..n-1  |  range(a,b)  |  range(a,b,step)
#  enumerate(x)    — (index, value) pairs
#  zip(a, b)       — pair items from two iterables
#  sorted(x)       — sorted copy  |  sorted(x, key=..., reverse=True)
#  reversed(x)     — reverse iterator
#  any(iterable)   — True if at least one element is truthy
#  all(iterable)   — True if every element is truthy
#  isinstance(obj, type)
#  print(*args, sep=" ", end="\n")
#  input(prompt)   — read string from stdin


# ------------------------------------------------------------
# QUICK PRACTICE EXERCISES
# ------------------------------------------------------------
#
# 1. Write a function that returns the factorial of n using recursion.
# 2. Given a list of words, return a dict mapping each word to its length.
# 3. Create a class Rectangle with width and height; add methods for
#    area() and perimeter(), and a __str__ for pretty printing.
# 4. Read a text file, count how many times each word appears, and
#    print the top 5 most common words.
# 5. Write a generator function that yields Fibonacci numbers up to n.
