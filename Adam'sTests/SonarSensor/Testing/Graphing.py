from csv import reader
from matplotlib import pyplot
import os, glob, sys

def timeSeriesSonar(filename):



    with open(filename, 'r') as f:

        data = list(reader(f))
        time = [i[0] for i in data]
        sense1 = map(float, [i[1] for i in data])
        sense2 = map(float, [i[2] for i in data])
        sense3 = map(float, [i[3] for i in data])



        pyplot.plot(time, sense1, color='r')
        pyplot.plot(time, sense2, color='b')
        pyplot.plot(time, sense3, color='g')
        #pyplot.axhline((sum(sense1)/len(sense1)), color='r', linestyle='dashed', linewidth=2)

        pyplot.savefig('graph.png')


if len(sys.argv) > 1:
    filename = sys.argv[1]

    timeSeriesSonar(filename)

else:

    filename = max(glob.iglob('Logs/*.csv'), key=os.path.getctime)
    timeSeriesSonar(filename)


