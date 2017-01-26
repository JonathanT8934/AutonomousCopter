from csv import reader
from matplotlib import pyplot
import os, glob, sys

def timeSeriesSonar(filename):

    with open(filename, 'r') as f:

        data = list(reader(f))
        time = [i[0] for i in data]
        sense1 = map(float, [i[1] for i in data])
        # sense2 = map(float, [i[2] for i in data])
        # sense3 = map(float, [i[3] for i in data])
        avgSense1 = getAverageSense(sense1)

        pyplot.plot(time, avgSense1, color='g')
        pyplot.plot(time, sense1, color='r')
        # pyplot.plot(time, sense2, color='b')
        # pyplot.plot(time, sense3, color='g')
        pyplot.axhline((sum(sense1)/len(sense1)), color='r', linestyle='dashed', linewidth=2)
        # pyplot.axhline((sum(sense2)/len(sense2)), color='b', linestyle='dashed', linewidth=2)
        # pyplot.axhline((sum(sense3)/len(sense3)), color='g', linestyle='dashed', linewidth=2)

        pyplot.savefig('graph.png')

def getAverageSense(senseList):

    avgSense1 = []  # Take 1,2,3 values for 2. convert to avergae
    for i in range(len(senseList)):
        if i == 0:
            b = senseList[i]
            c = senseList[i + 1]
            a = (b+c)/2
        elif i == len(senseList)-1:
            a = senseList[i - 1]
            b = senseList[i]
            c = (a+b)/2

        else:
            a = senseList[i - 1]
            b = senseList[i]
            c = senseList[i + 1]

        avgSense1.append(round((a+b+c)/3,2))

    return avgSense1



if len(sys.argv) > 1:
    filename = sys.argv[1]

    timeSeriesSonar(filename)

else:
    filename = 'Logs/SonarTestingOutput-1485105228.47.csv'
    #filename = max(glob.iglob('Logs/*.csv'), key=os.path.getctime)
    timeSeriesSonar(filename)

