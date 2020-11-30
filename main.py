# Python program to create a table 
import matplotlib.pyplot as plt
import math
from WorldLogic.worldLogic import World, WORLD_SIZE, INIT_TEMP, INIT_AIR_POLLUTION, CellTypes
import tkinter as tk
from scipy import stats

Colors = {
    "C": "gray",
    "L": "brown",
    "G": "white",
    "F": "green",
    "S": "blue"
}

GENERATIONS = 366


# GENERATIONS = 40

class Table:
    def __init__(self, world, element, genLabel):
        self.tempAverages = [None] * GENERATIONS
        self.tempStd = [None] * GENERATIONS
        self.maxTemp = [None] * GENERATIONS
        self.minTemp = [None] * GENERATIONS
        self.airPollutionAverages = [None] * GENERATIONS
        self.airPStd = [None] * GENERATIONS
        self.maxAirPollution = [None] * GENERATIONS
        self.minAirPollution = [None] * GENERATIONS

        self.cells = [[None] * WORLD_SIZE for i in range(WORLD_SIZE)]
        self.world = world
        self.root = root
        self.genLabel = genLabel
        gen = self.world.currGen
        # code for creating table
        tempSum = 0

        for r in range(WORLD_SIZE):
            for c in range(WORLD_SIZE):
                currCell = gen[r][c]
                color = Colors[currCell.cType]
                cellLabel = tk.Label(element, text="{:.1f}".format(currCell.temp), width=5, fg='black', bg=color,
                                     font=('Arial', 6, 'bold'), borderwidth=0.2)
                # entry = tk.Entry(root, width=5, fg='black', bg=color,
                #                font=('Arial', 5, 'bold'))

                cellLabel.grid(row=r, column=c)
                self.cells[r][c] = cellLabel
                tempSum += currCell.temp

        self.minTemp[0] = INIT_TEMP
        self.maxTemp[0] = INIT_TEMP
        self.minAirPollution[0] = 0
        self.maxAirPollution[0] = 0
        self.tempAverages[0] = INIT_TEMP
        self.airPollutionAverages[0] = INIT_AIR_POLLUTION

    def updateGen(self):
        if world.genNum >= GENERATIONS - 1:
            print(stats.pearsonr(self.airPollutionAverages, self.tempAverages))
            self.showGraphs()

            return
        else:
            world.calcNextGen()
            gen = world.currGen
            airPollutionlst = []
            tempLst = []

            for r in range(WORLD_SIZE):
                for c in range(WORLD_SIZE):
                    currCell = gen[r][c]
                    currLabel = self.cells[r][c]
                    color = Colors[currCell.cType]
                    currLabel.config(bg=color, text="{:.1f}".format(currCell.temp))

                    if currCell.cType in [CellTypes.LAND.value, CellTypes.CITY.value, CellTypes.FOREST.value]:
                        tempLst.append(currCell.temp)
                        airPollutionlst.append(currCell.airPollution)

            self.genLabel.config(text="Day-{}".format(world.genNum))
            tempAvg = average(tempLst)
            self.tempAverages[world.genNum] = tempAvg
            self.tempStd[world.genNum] = std_dev(tempLst, tempAvg)
            airPAvg = average(airPollutionlst)
            self.airPollutionAverages[world.genNum] = airPAvg
            self.airPStd[world.genNum] = std_dev(airPollutionlst, airPAvg)
            self.maxTemp[world.genNum] = max(tempLst)
            self.minTemp[world.genNum] = min(tempLst)
            self.maxAirPollution[world.genNum] = max(airPollutionlst)
            self.minAirPollution[world.genNum] = min(airPollutionlst)
            self.printDailyStatus()
            self.root.after(1, self.updateGen)

    def printDailyStatus(self):
        print("Day-{}".format(world.genNum))
        print("Temperature range is [{}-{}].".format(
            "{:.1f}".format(self.minTemp[world.genNum]),
            "{:.1f}".format(self.maxTemp[world.genNum])))
        print("The average temperature is {}.".format("{:.1f}".format(self.tempAverages[world.genNum])))
        print("The standard deviation for temperature is {}".format("{:.1f}".format(self.tempStd[world.genNum])))
        print("Air pollution range is [{}-{}].".format(
            "{:.1f}".format(self.minAirPollution[world.genNum]),
            "{:.1f}".format(self.maxAirPollution[world.genNum])))
        print("The average air pollution is {}.".format("{:.1f}".format(self.airPollutionAverages[world.genNum])))
        print("The standard deviation for air pollution is {}".format("{:.1f}".format(self.airPStd[world.genNum])))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def showGraphs(self):

        plt.plot(normalize(self.tempAverages), label="average temp")
        plt.legend()
        plt.title("Temperature normalized statistics in cities,lands and forests over a year")
        plt.figure()

        plt.plot(normalize(self.airPollutionAverages), label="average air pollution")
        plt.legend()
        plt.title("Air pollution normalized statistics in cities,lands and forests over a year")
        plt.show()


average = lambda data: sum(data) / len(data)
variance = lambda data, avg: sum([x ** 2 for x in [i - avg for i in data]]) / float(len(data))
std_dev = lambda data, avg: math.sqrt(variance(data, avg))


def normalize(data):
    avg = average(data)
    std = std_dev(data, avg)
    if std == 0:
        return [x - avg for x in data]
    else:
        return [(x - avg) / std for x in data]


world = World()

# create root window
root = tk.Tk()
root.title('World Simulation')

label = tk.Label(root, text="Day-{}".format(world.genNum))
label.pack()
fr = tk.Frame(root)
t = Table(world, fr, label)
fr.pack()
root.after(5000, t.updateGen)
# t.updateGen()

root.mainloop()
