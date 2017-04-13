# Import the modules
import sys
import random


def importStamps():
    return [line.rstrip('\n') for line in open('TimeStamps.txt')]


def calcNumbers(stamps):
    print(stamps[0])

    randomNums = []
    subtractionList = []

    i = 0
    for x in range(len(stamps) - 2):
        stamps[i] = float(stamps[i + 1]) - float(stamps[i])
        subtractionList.append(round(float(stamps[i]), 2))
        i += 1


    for x in subtractionList:
        print(x)

    i = 0
    for x in range(len(subtractionList) - 1):
        if float(subtractionList[i]) > float(subtractionList[i+1]):
            randomNums.append(1)
        else:
            randomNums.append(0)
        i += 1

    return randomNums

list = importStamps()
numbers = calcNumbers(list)
print(numbers[0])
i = 0
for x in numbers:
    print(numbers[i])
    i += 1
print(i)
