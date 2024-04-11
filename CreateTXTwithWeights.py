#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 14:24:35 2024

@author: stijnvanderwal
"""

import os
import txtfromcsv
import numpy as np

# Constants
# Values rectified by https://doi.org/10.1175/1520-0450(1988)027%3C0550:SDOWSA%3E2.0.CO;2

"""
Here the user can specify the sets of paramters for which a txt file will be created.
By giving a list of numbers, the code creates a txt file for each combination
The name of the TXT file will represent the combination of variables and is 
structured as follows: InstanceName_Ws{windspeed}_Wd{windDirection}_o{nrObservations}.txt
"""

WIND_SPEED_FORECAST = [4,7] # in ms^-1
WIND_DIRECTION_FORECAST = [0,120,240] # in degrees
nrLoadlevels = 10
nrObservations = 9

# Function to create a folder if it doesn't exist
def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    
# This function converts a 4D matrix with the specified structure to a 2D matrix with 
# the structure that can be understood by the SA-ILP algirthm.
def convert4Dto2D(travelMatrix4D):
    nrCustomers, nrLoadlevels, nrObservations = travelMatrix4D.shape[0],travelMatrix4D.shape[2],travelMatrix4D.shape[3]
    nr_edges = nrCustomers**2
    nr_columns = nrLoadlevels * nrObservations
    travelTimeMatrix2D = np.zeros((nr_edges, nr_columns))
    
    for n in range(nr_edges):
        for m in range(nr_columns):
            if n//nrCustomers != n%nrCustomers:
                travelTimeMatrix2D[n,m] = travelMatrix4D[n//nrCustomers, n%nrCustomers, m//nrObservations, m%nrObservations]
    return travelTimeMatrix2D

# Function to generate .txt files using TXTfromCSV class
def generate_txt_file(output_folder, input_file, WIND_SPEED_FORECAST, 
                      WIND_SPEED_SIGMA, WIND_DIRECTION_FORECAST, WIND_DIRECTION_SIGMA):
    
    customers, distances = txtfromcsv.csvImporter(input_file)
    
    # this returns a 4D matrix
    travelMatrixToPrint = txtfromcsv.computeTravelTimeMatrixWithWeights(customers, distances, 
                            WIND_SPEED_FORECAST, WIND_SPEED_SIGMA, WIND_DIRECTION_FORECAST, WIND_DIRECTION_SIGMA, 
                            nrObservations, nrLoadlevels)
    output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + f"_Ws{WIND_SPEED_FORECAST}_Wd{WIND_DIRECTION_FORECAST}_weights.txt")
    txtfromcsv.write_travel_time_matrix_to_file(travelMatrixToPrint, len(customers), nrLoadlevels, nrObservations, output_file)
    
# The function makes sure we use each instance from the input folder
def generate_txt_files_from_folder(output_folder, input_folder, WIND_SPEED_FORECAST, 
                      WIND_SPEED_SIGMA, WIND_DIRECTION_FORECAST, WIND_DIRECTION_SIGMA):
    create_folder(output_folder)
    for root, _, files in os.walk(input_folder):
        for file in files:
            print(f"Busy converting {file}")
            input_file = os.path.join(root, file)
            generate_txt_file(output_folder, input_file, WIND_SPEED_FORECAST, 
                                  WIND_SPEED_SIGMA, WIND_DIRECTION_FORECAST, WIND_DIRECTION_SIGMA)

def main():
    output_folder = "/Users/stijnvanderwal/Documents/GitHub/Simulator/TestWithWeights/TXTfiles"
    input_folder = "/Users/stijnvanderwal/Documents/GitHub/Simulator/TestWithWeights/CSVfiles"
    for windSpeed in WIND_SPEED_FORECAST:
        for windDirection in WIND_DIRECTION_FORECAST:
            print(f"Now starting for windspeed:{windSpeed}, dir:{windDirection}")
            if windSpeed<5:
                windSsigma = 0.4*windSpeed
                windDsigma = 0.32/windSpeed*(180/np.pi)
            else:
                windSsigma = 0.08*windSpeed
                windDsigma = 0.065/windSpeed*(180/np.pi)
            generate_txt_files_from_folder(output_folder, input_folder, windSpeed,windSsigma, windDirection, windDsigma)

if __name__ == "__main__":
    main()
