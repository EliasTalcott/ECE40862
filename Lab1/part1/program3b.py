#!/usr/bin/env python

import random

# Generate a random integer between 0 and 10
num = random.randint(0, 10)

# Give three guesses
for i in range(3):
    while True:
        try:
            user_num = input("Enter your guess: ")
            user_num = int(user_num)
            if 0 <= user_num <= 10:
                break
            else:
                print("Please make a guess between 0 and 10")
        except ValueError:
            print("'{}' cannot be cast to an integer".format(user_num))
    if user_num == num:
        print("You win!")
        break

if user_num != num:
    print("You lose!")
