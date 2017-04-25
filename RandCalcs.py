# Import the modules
import sys
import random
import urllib2


#does a webcall to a php file asking for x number of stamps
#then stores the time stamps into a list to be used by later functions
def importStamps(x):
    words = urllib2.urlopen("http://cs.iusb.edu/~djcassid/server.php?numStamps=" + str(x)) .read()
    words = words.strip().split()
    #print(words[0])
    return words


#takes the list of stamps and current spot in the list
#gets subtracted from the next stamp in the list
#this represents the time elapsed which is stored in a new list subtractionList
#this new list then does a comparison of elapsed times where if the
#current is greater we get a 1 else we get a 0
def calcNumbers(stamps):
    randomNums = []
    subtractionList = []
    i = 0
    for x in range(len(stamps) - 1):
        stamps[i] = float(stamps[i + 1]) - float(stamps[i])
        subtractionList.append(round(float(stamps[i]), 2))
        i += 1

    i = 0
    for x in range(len(subtractionList) -1):
        if float(subtractionList[i]) > float(subtractionList[i+1]):
            randomNums.append(1)
        else:
            randomNums.append(0)
        i += 1
    return randomNums

#here we simply create a unpacked byte number but its called
#packed because logically we packed 8 bits together
def packBits(BitList):
    packedList = []
    for x in range(0,len(BitList)-7,8):
        #iterates 0 to length of BitList on steps of 8
        packedList.append(str(BitList[x])+str(BitList[x+1]) +
            str(BitList[x + 2]) + str(BitList[x + 3]) +
            str(BitList[x + 4]) + str(BitList[x + 5]) +
            str(BitList[x + 6]) + str(BitList[x + 7]))

    return packedList

#here we simply turn a byte into a normal integer
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

    return numList

#here we make a call to cpm.php to get 60 stamps that we then calculate the
#total time elapsed and throw out any timestamp that is more than 30 seconds
#after the last one. Then we take that time and convert from seconds to minutes
#and divide the count of our stamps by the total minutes to find the average
#counts per minute
def calcTime():
    stamps = urllib2.urlopen("http://cs.iusb.edu/~djcassid/cpm.php").read()
    stamps = stamps.strip().split()
    subtractionList = []

    i = 0
    for x in range(len(stamps) - 1):
        stamps[i] = float(stamps[i + 1]) - float(stamps[i])
        subtractionList.append(round(float(stamps[i]), 2))
        i += 1

    count = 1
    timeSum = 0
    i = 0
    for x in subtractionList:
        if float(subtractionList[i]) < 30:
            count = count + 1
            timeSum = timeSum + subtractionList[i]
        i += 1

    minutesCount = float(timeSum / 60)
    cpm = round(float(count / minutesCount), 2)
    print("total time in seconds = " + str(timeSum))
    print("total number of timestamps counted = " + str(count))
    print("timestamp count per minute = " + str(cpm))

    return cpm

#calls functions to return an integer list
def packedListCall(x):
    unpackedList = []
    try:
        unpackedList = importStamps((x*8)+2)
        unpackedList = calcNumbers(unpackedList)
        unpackedList = packBits(unpackedList)
        unpackedList = unpackBits(unpackedList)
        return unpackedList
    except:
        return unpackedList


#calls functions to return a list of bytes
def unpackedListCall(x):
    packedList = []
    try:
        packedList = importStamps((x*8)+2)
        packedList = calcNumbers(packedList)
        packedList = packBits(packedList)
        return packedList
    except:
        return packedList

#example main calls
list = unpackedListCall(1)
list2 = packedListCall(1)
print(list[0])
print(list2[0])
calcTime()
