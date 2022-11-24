import sys
import numpy as np
import time

def readFile(nameOfFile):
    file = open(nameOfFile, "r")
    numberOfLines = int(file.readline())
    array = []
    for i in range (0, numberOfLines):
        array.append(file.readline().strip())
        #strip removes newline
    file.close()
    return array

def splitInto2dArray(array):
    newArray = []
    for i in array:
        #split string by :
        a = i.split(":")
        name = a[0]
        typeOf = a[1] #distinct or cont
        min = a[2]
        if len(a) == 6: #means this is events.txt
            max = a[3]
            weight = a[4]
            #print(a)
            newArray.append([name, typeOf, min, max, weight])
        else:
            #means this is stats.txt
            weight = a[3]
            newArray.append([name, typeOf, min])
            #actually name, mean, stddev but reused var names
    #print(newArray)
    return newArray

def generateEvents(arrayEvents, arrayStats, numDays):
    generatedArray = []
    for j in range(0, numDays):
        arrayNew = []
        for i in range(0, len(arrayStats)):
            name = arrayStats[i][0]
            mean = float(arrayStats[i][1])
            stddev = float(arrayStats[i][2])
            #print(mean)
            arr = np.random.normal(mean, stddev, 1)
            #uses gaussian distribution

            #prevent number being out of bounds
            #regenerate if it is.
            while arr[0] < float(arrayEvents[i][2]):
                arr = np.random.normal(mean, stddev, 1)
            if len(arrayEvents[i][3]) != 0:
                while arr[0] > float(arrayEvents[i][3]):
                   arr = np.random.normal(mean, stddev, 1)

            if (arrayEvents[i][1] == "C"):
                #if continuous, round to 2dp
                arrayNew.append([name, round(arr[0],2)])
            else:
                #else whole number
                arrayNew.append([name, round(arr[0])])
        generatedArray.append(["Day " + str(j+1), arrayNew])
        
    #for i in generatedArray:
        #print(i)
    return generatedArray

def printArrayEvents(array):
    print("Event, Type, minimum, maximum, weight")
    for i in array:
        print(i[0], end = ", ")
        if i[1] == "C":
            print("Continuous", end = ", ")
        elif i[1] == "D":
            print("Discrete", end = ", ")
        print(i[2], end = ", ")
        if len(i[3]) != 0:
            print(i[3], end = ", ")
        else:
            print("null", end = ", ")
        print(i[4],end = "")
        print() #line break
        
def printArrayStats(array):
    print("Event, mean, std Deviation")
    for i in array:
        print(i[0], end = ", ")
        print(i[1], end = ", ")
        print(i[2], end = "\n")

def checkInconsistencies(nameOfEvents, nameOfStats, arrayEvents, arrayStats):
    file1 = open(nameOfEvents, "r")
    file2 = open(nameOfStats, "r")
    isConsistent = True
    reason = None
    #case 1, value given in first line is not consistent
    if (file1.readline()) != (file2.readline()):
        isConsistent = False
        reason = "Value given in first line is inconsistent"
    else:
    #case 2, event names are different
        for i in range(0, len(arrayEvents)):
            if (arrayEvents[i][0] != arrayStats[i][0]):

                isConsistent = False
                reason = "Event names are different"
    file2.close()
    file1.close()
    return isConsistent, reason

def logGeneratedEventsToFile(generatedEvents, nameOfEvents, filename = "eventlog.txt"):
    file = open(filename, "w")
    for i in generatedEvents:
        file.write(i[0] + "\n")
        file3 = open(nameOfEvents, "r")
        numOfLines = file3.readline()
        file3.close()
        for j in range(0, int(numOfLines)):
            file.write(i[1][j][0] + ": " + str(i[1][j][1]) + "\n")
        file.write("\n")

    file.close()

#analysis engine
def analyzeGenerated(generatedEvents, arrayEvents):
    #store totals by event
    #name of events
    arrayAnalysis = []
    
    for i in range(0,len(arrayEvents)):
        event = arrayEvents[i][0]
        count = 0
        totalNumber = 0
        arrayForSD = []
        for j in generatedEvents:
            count += 1
            totalNumber += j[1][i][1]
            arrayForSD.append(j[1][i][1])

        mean = round(totalNumber/count, 2)
        stddev = round(np.std(arrayForSD), 2)
        arrayAnalysis.append([event, mean, stddev])
    print("\nEvent, Mean, Std Deviation")
    for i in arrayAnalysis:
        print(i[0] + ", " + str(mean)+", " + str(stddev))
    return arrayAnalysis

def alertEngine(alertGeneratedEvents, arrayAnalysis, sumOfWeights):
    threshold = sumOfWeights * 2
    #if exceeded, raise alert.
    #print(threshold)
    #print(arrayAnalysis)
    #print(alertGeneratedEvents)
    totalAnomalyCount = 0
    for i in range(0, len(alertGeneratedEvents)):
        anomalyCount = 0
        for j in range(0, len(alertGeneratedEvents[i][1])):
            #print(alertGeneratedEvents[i][1][j][1])
            #compare against arrayAnalysis[j]
            mean = arrayAnalysis[j][1]
            stdDev = arrayAnalysis[j][2]
            #print(alertGeneratedEvents[i][0]) #day
            #print(alertGeneratedEvents[i][1][j][1]) #numOfEvents
            #print(mean)
            #print(stdDev)
            anomaly = abs(alertGeneratedEvents[i][1][j][1] - mean) / stdDev
            #print("anomaly value: ", end= "")
            #print(anomaly)
            anomalyCount += anomaly
        print("Anomaly Count for " + alertGeneratedEvents[i][0] + ": " + str(round(anomalyCount,2)))
        if anomalyCount >= threshold:
            print("Intrusion Detected on " + alertGeneratedEvents[i][0])
            totalAnomalyCount += 1
        print()
    print()
    return totalAnomalyCount


def writeAnalysisToFile(arrayAnalysis, filename = "analysisLog.txt"):
    #print(arrayAnalysis)
    file = open(filename, "w")
    for i in arrayAnalysis:
        file.write(i[0] + "\n")
        file.write("Mean: " + str(i[1]) +", Standard Deviation: " +str(i[2])+ "\n")
        file.write("\n")

    file.close()

def main():
    
    #read files
    #nameOfEvents = sys.argv[1] 
    nameOfEvents = "Events.txt"
    #nameOfStats = sys.argv[2]
    nameOfStats = "Stats.txt"
    #numOfDays = int(sys.argv[3])
    numOfDays = 8

    print("Reading " + nameOfEvents + "\n")
    arrayEvents = splitInto2dArray(readFile(nameOfEvents))
    printArrayEvents(arrayEvents)
    #print(arrayEvents)
    time.sleep(1) 
    print("\nReading " + nameOfStats + "\n")
    arrayStats = splitInto2dArray(readFile(nameOfStats))
    printArrayStats(arrayStats)
    reason = None
    
    #detect inconsistency here
    isConsistent, reason = checkInconsistencies(nameOfEvents, nameOfStats, arrayEvents, arrayStats)
    if (isConsistent == False):
        print("\nInconsistencies between files detected. Program will exit shortly.")
        print("Reason: " + str(reason), end = "\n\n")
        time.sleep(2)
        exit()
    time.sleep(1)
    print("\nGenerating events\n")
    generatedEvents = generateEvents(arrayEvents, arrayStats, numOfDays)
    time.sleep(1)
    logGeneratedEventsToFile(generatedEvents, nameOfEvents)
    print("Events generated, stored in eventlog.txt\n")
    time.sleep(1)
    print("Proceeding to analysis")
    arrayAnalysis = analyzeGenerated(generatedEvents, arrayEvents)
    writeAnalysisToFile(arrayAnalysis)

    print("\nAnalysis complete.\n")
    time.sleep(1)
    print("Proceeding to alert engine.")
    continueRunning = True
    while (continueRunning == True):
        alertFileName = input("Enter a file name for the alert engine, or nothing to exit: ")

        if alertFileName == '':
            print("Program Exiting.")
            continueRunning = False
            exit()

        arrayAlertFile = splitInto2dArray(readFile(alertFileName))
        alertNumDays = input("Enter a number of days, or nothing to exit: ")

        if alertNumDays == '':
            print("Program Exiting.")
            continueRunning = False
            exit()
        print()
        
        alertGeneratedEvents = generateEvents(arrayEvents, arrayAlertFile, int(alertNumDays))

        sumOfWeights = 0
        for i in arrayEvents:
            sumOfWeights += int(i[4])
        logFileName = alertFileName[:-4] + "EventLog.txt" 
        logGeneratedEventsToFile(alertGeneratedEvents, nameOfEvents, logFileName)
        print("\nEvents Generated, stored in "+ logFileName, end = "\n\n")
        print("Threshold for Intrusion Detection: " + str(sumOfWeights * 2), end="\n\n")
        totalAnomaly = alertEngine(alertGeneratedEvents, arrayAnalysis, sumOfWeights)
        print("Alert engine analysis complete.")
        if totalAnomaly < 1:
            print("\nNo anomalies found!\n")
        else:
            print()
            print(totalAnomaly, end = " ")
            print("anomalie(s) found!\n")

    #this line should never be hit
    print("Program Exiting.")

if __name__ == "__main__":
    main()