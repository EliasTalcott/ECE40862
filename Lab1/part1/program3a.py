#!/usr/bin/env python

# Ask user for a number
while True:
    try:
        user_num = input("How many Fibonacci numbers would you like to generate? ")
        user_num = int(user_num)
        if user_num > 0:
            break
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("'{}' cannot be cast to an integer".format(user_num))

# Generate and print Fibonacci sequence
a = [1, 1]
n = 2
while n < user_num:
    a.append(a[n - 1] + a[n - 2])
    n += 1
print(a[:user_num])
