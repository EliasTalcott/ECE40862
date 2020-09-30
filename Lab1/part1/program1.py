#!/usr/bin/env python

from datetime import date

# Get user's name
name = input("What is your name? ")

# Get user's age as an integer
while True:
    try:
        age = input("What is your age? ")
        age = int(age)
        if age >= 0:
            break
        else:
            print("You cannot be less than 0 years old..")
    except ValueError:
        print("'{}' cannot be cast to an integer".format(age))

# Get current year
year = date.today().year

# Print when user will be 100
print("{} will be 100 years old in the year {}".format(name, year + 100 - age))
