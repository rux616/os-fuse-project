# Import the modules
import sys
import random


def importStamps():
    return [line.rstrip('\n') for line in open('TimeStamps.txt')]


def calcNumbers(stamps):
    print(stamps[0])

    i = 0
    for x in range(len(stamps) - 1):
        stamps[i] = float(stamps[i + 1]) - float(stamps[i])
        stamps[i] = round(float(stamps[i]), 2)
        i += 1
    stamps.pop()

    print(stamps[0])
    return stamps


list = importStamps()
numbers = calcNumbers(list)
print(numbers[0])
i = 0
for x in numbers:
    print(numbers[i])
    i += 1
print(i)
