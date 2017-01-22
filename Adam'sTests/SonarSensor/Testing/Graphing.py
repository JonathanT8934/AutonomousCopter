from csv import reader

import matplotlib
matplotlib.use("WXAgg")
from matplotlib import pyplot
import os, glob, sys

def timeSeriesSonar(filename):



    with open(filename, 'r') as f:
        data = list(reader(f))
        time = [i[0] for i in data]
        sense1 = [i[1] for i in data]

        pyplot.plot(range(len(time)), sense1)
        pyplot.show()



if len(sys.argv) > 1:
    filename = sys.argv[1]

    timeSeriesSonar(filename)

else:

    filename = max(glob.iglob('Logs/*.csv'), key=os.path.getctime)
    timeSeriesSonar(filename)


