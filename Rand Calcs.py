# Import the modules
import sys
import random

globalIndex = 0

def importStamps():
    return [line.rstrip('\n') for line in open('TimeStamps.txt')]


def calcNumbers(stamps):
    #print(stamps[0])

    randomNums = []
    subtractionList = []
    #print(len(stamps))
    i = 0
    for x in range(len(stamps) - 1):
        stamps[i] = float(stamps[i + 1]) - float(stamps[i])
        subtractionList.append(round(float(stamps[i]), 2))
        i += 1
    stamps.clear()

    #for x in subtractionList:
    #    print(x)
    #print(len(subtractionList))
    i = 0
    for x in range(len(subtractionList) -1):
        if float(subtractionList[i]) > float(subtractionList[i+1]):
            randomNums.append(1)
        else:
            randomNums.append(0)
        i += 1
    subtractionList.clear
    return randomNums


def packBits(BitList):
    packedList = []
    #print(len(BitList))
    for x in range(0,len(BitList)-7,8):
        #iterates 0 to length of BitList on steps of 8
        packedList.append(str(BitList[x])+str(BitList[x+1]) +
            str(BitList[x + 2]) + str(BitList[x + 3]) +
            str(BitList[x + 4]) + str(BitList[x + 5]) +
            str(BitList[x + 6]) + str(BitList[x + 7]))

    #for x in packedbits:
    #   print(x)
    BitList.clear()
    return packedList


def unpackBits (packedList):
    numList = []
    tempList = []
    for x in range(len(packedList)):
        tempStr = str(packedList[x].split(','))
        tempList.append(tempStr[2])
        tempList.append(tempStr[3])
        tempList.append(tempStr[4])
        tempList.append(tempStr[5])
        tempList.append(tempStr[6])
        tempList.append(tempStr[7])
        tempList.append(tempStr[8])
        tempList.append(tempStr[9])

    #for x in tempList2:
    #   print(x)
    #print(len(tempList2))

    for x in range(0, len(tempList) - 7, 8):
        sum = 0
        sum = sum + (int(int(tempList[x + 7])))
        sum = sum + (int(int(tempList[x + 6])) * 2)
        sum = sum + (int(int(tempList[x + 5])) * 4)
        sum = sum + (int(int(tempList[x + 4])) * 8)
        sum = sum + (int(int(tempList[x + 3])) * 16)
        sum = sum + (int(int(tempList[x + 2])) * 32)
        sum = sum + (int(int(tempList[x + 1])) * 64)
        sum = sum + (int(int(tempList[x])) * 128)
        numList.append(sum)

    #for x in numList:
    #    print(x)

    tempList.clear()
    return numList


def newlist():
    list = importStamps()
    list = calcNumbers(list)
    list = packBits(list)
    return list


#example main calls
list = newlist()
print(list[0])
numbersList = unpackBits(list)
print(numbersList[0])

