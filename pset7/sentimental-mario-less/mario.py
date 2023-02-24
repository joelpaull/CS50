# TODO

from cs50 import get_int

height = 0
while height not in range(1,9):
    height = get_int("What height pyramid would you like? 1-8\n")
count = 1
while count <= height:
    for i in range(0, height - count):
        print(" ", end = "")
    for i in range(0, count):
        print("#", end = "")
    print()
    count += 1

