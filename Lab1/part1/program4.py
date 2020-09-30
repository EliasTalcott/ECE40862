#!/usr/bin/env python

# Make dictionary of birthdays and print
birthdays = {"Albert Einstein": "03/14/1879", "Benjamin Franklin": "01/17/1706", "Ada Lovelace": "12/10/1815"}
print("Welcome to the birthday dictionary. We know the birthdays of:")
for key in birthdays:
    print(key)

# Ask for birthday request
while True:
    try:
        request = input("Who's birthday do you want to look up? ")
        birthday = birthdays[request]
        break
    except KeyError:
        print("{} is not in our birthday dictionary".format(request))

# Print the birthday
print("{}'s birthday is {}".format(request, birthday))
