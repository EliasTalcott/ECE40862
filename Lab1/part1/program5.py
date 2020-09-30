#!/usr/bin/env python

class FindPairsToAdd:
    def __init__(self, num_list):
        self.num_list = num_list
        self.index_one = None
        self.index_two = None

    def find_pairs(self, num):
        for i, num1 in enumerate(self.num_list):
            for j, num2 in enumerate(self.num_list[i+1:]):
                if num1 + num2 == num:
                    print("index1={} index2={}".format(i, j + i + 1))


if __name__ == "__main__":
    # Initialize number list and FindPairsToAdd object
    a = [10, 20, 10, 40, 50, 60, 70]
    thing = FindPairsToAdd(a)

    # Print list of indices for which the elements add to a desired number
    while True:
        try:
            user_num = input("What is your target number? ")
            user_num = int(user_num)
            break
        except ValueError:
            print("'{}' cannot be cast to an integer".format(user_num))
    thing.find_pairs(user_num)
