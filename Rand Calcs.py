# Import the modules
import sys
import random


def importStamps():
    return [line.rstrip('\n') for line in open('TimeStamps.txt')]


def calcNumbers(stamps):
    #print(stamps[0])

    randomNums = []
    subtractionList = []

    i = 0
    for x in range(len(stamps) - 2):
        stamps[i] = float(stamps[i + 1]) - float(stamps[i])
        subtractionList.append(round(float(stamps[i]), 2))
        i += 1


    #for x in subtractionList:
    #    print(x)

    i = 0
    for x in range(len(subtractionList) - 1):
        if float(subtractionList[i]) > float(subtractionList[i+1]):
            randomNums.append(1)
        else:
            randomNums.append(0)
        i += 1

    return randomNums

def packBits(BitList):
    packedbits = []
    #print(len(BitList))
    i = 0
    for x in range(len(BitList)-7):
        packedbits.append(str(BitList[i])+str(BitList[i+1]) +
            str(BitList[i + 2]) + str(BitList[i + 3]) +
            str(BitList[i + 4]) + str(BitList[i + 5]) +
            str(BitList[i + 6]) + str(BitList[i + 7]))
    #    i += 8

    print(packedbits[0])
    return packedbits

def newlist():
    list = importStamps()
    list = calcNumbers(list)
    list = packBits(list)
    return list

list = newlist()
print(list[0])
