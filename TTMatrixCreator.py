#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 09:50:06 2024

@author: stijnvanderwal

This code is meant to create matrices that are filled with travel time 'observations'
to be used in the SA-ILP algorithm for solving the SVRPLTT
"""

import VRP
import Simulator
import numpy as np
import random
import time

start_time = time.time()

writeFileCSV = False
writeFileTXT = True
filename = "Test22feb3/Fukuoka_full.csv"
#filename = "/Users/stijnvanderwal/Documents/GitHub/SA-ILP_new/instances/large/fukuoka_full.csv"
#filename = "/Users/stijnvanderwal/Documents/GitHub/Simulator/Solutions/Fukuoka_01.csv"
numberCustomers = 101
numberLoadlevels = 10
numberObservations = 20
seednr = 42

# values rectified by https://doi.org/10.1175/1520-0450(1988)027%3C0550:SDOWSA%3E2.0.CO;2
windSpeedForecast, windSpeedSigma = 3.75, 0.4*3.75
windDirectionForecast, windDirectionSigma = 60/180*np.pi, 15/180*np.pi

customers, distanceMatrix = Simulator.csvImporter(filename = filename)

print(distanceMatrix)

i=0
customers = customers[i:i+numberCustomers]

def TravelTimeComputer(loadLevel, travelDistance,slope, windSpeed, windAngle):
    mass = 140 + (loadLevel+0.5)* (290-140)/numberLoadlevels
    #output is in m/s
    driveSpeed = VRP.computeSpeed(mass, slope, windSpeed, windAngle)
    
    return travelDistance/driveSpeed/60

try:
    scale = windSpeedSigma**2 / windSpeedForecast
    shape = windSpeedForecast / scale
except:
    shape = 0
    
#print(len(customers))
    
nrEdges = numberCustomers**2
nrColumns = numberObservations*numberLoadlevels
travelTimeMatrix = np.zeros((nrEdges, nrColumns))

random.seed(seednr)
for n in range(nrColumns):
    if n%(nrColumns/10) ==0:
        print(f"{n}/{nrColumns}")
    if shape == 0:
        windSpeed = windSpeedForecast
    else:
        windSpeed = max(0,random.gammavariate(shape, scale))
    windDirection = random.normalvariate(windDirectionForecast,windDirectionSigma)
    
    loadLevel = int(n//numberObservations)
    
    for custStart in range(len(customers)):
        for custEnd in range(len(customers)):
            if custStart != custEnd:
                travelDistance = distanceMatrix[custStart,custEnd]
                currentCustomer = customers[custStart]
                nextCustomer = customers[custEnd]
                heading = np.arctan((nextCustomer.y-currentCustomer.y)/(nextCustomer.x-currentCustomer.x))
                windAngle = windDirection-heading
                slope = (nextCustomer.h-currentCustomer.h)/travelDistance
                #print(custStart*numberCustomers + custEnd)
                travelTimeMatrix[custStart*numberCustomers + custEnd,n] = np.round(TravelTimeComputer(loadLevel, travelDistance, slope, windSpeed, windAngle),2)

print(travelTimeMatrix)

if writeFileCSV == True:
    import csv
    
    with open('file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for edge in range(nrEdges):
            for n in range(numberObservations):
                stringRow = travelTimeMatrix[edge, :]
            writer.writerow(stringRow)

if writeFileTXT == True:
    with open('Test22feb3/Fukuoka_6.txt', 'w') as file:
        file.write(f"{numberCustomers}, {numberLoadlevels}, {numberObservations}, Windspeed: {windSpeedForecast}:{windSpeedSigma}, Winddirection:{np.round(windDirectionForecast,1)}:{np.round(windDirectionSigma,1)}, seed={seednr}  \n")
        for n in range(nrEdges):
            for c in range(nrColumns):
                file.write(str(travelTimeMatrix[n,c]))
                if c<nrColumns-1:
                    file.write(",")
            file.write("\n")

end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")
                    