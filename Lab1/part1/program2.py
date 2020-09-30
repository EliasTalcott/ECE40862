#!/usr/bin/env python

import random

# Generate and print a random list of 10 integers between 1 and 100
a = [random.randint(1, 100) for _ in range(10)]
print(a)

# Ask user for a number
while True:
    try:
        user_num = input("Enter number: ")
        user_num = int(user_num)
        break
    except ValueError:
        print("'{}' cannot be cast to an integer".format(user_num))

# Remove numbers higher than or equal to user's number and print
a = [num for num in a if num < user_num]
print(a)
