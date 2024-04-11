#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 14:22:33 2024

@author: stijnvanderwal
"""

import os
import txtfromcsv

windSpeed_forecast = 5
windSpeed_sigma = 1
windDirection_forecast = 20
windDirection_sigma = 10
numberObservations = 2
numberLoadlevels = 10

# Function to create a folder if it doesn't exist
def create_folder(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

# Function to generate .txt files using TXTfromCSV class
def generate_txt_file(outputFolder, inputFile):
    customers, distances = txtfromcsv.csvimporter(inputFile)
    travelTimeMatrix = txtfromcsv.computeTravelTimeMatrix(customers, distances, 
                                                          windSpeed_forecast, windSpeed_sigma, windDirection_forecast, windDirection_sigma, 
                                                          numberObservations, numberLoadlevels)
    txtfromcsv.write_travel_time_matrix_to_file(travelTimeMatrix, len(customers), numberLoadlevels, numberObservations, outputFolder)
    
def generateTXTfromFolder(outputFolder, inputFolder):
    for file in inputFolder:
        generate_txt_file(outputFolder, file)

def main():
    outputFolder = "/Users/stijnvanderwal/Documents/GitHub/Simulator"
    inputFolder = "/Users/stijnvanderwal/Documents/GitHub/SA-ILP_new/instances/small"
    create_folder(outputFolder)
    generateTXTfromFolder(outputFolder, inputFolder)

if __name__ == "__main__":
    main()
