#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:03:01 2024

@author: stijnvanderwal
"""

import os
import txtfromcsv
import numpy as np

# Constants
# Values rectified by https://doi.org/10.1175/1520-0450(1988)027%3C0550:SDOWSA%3E2.0.CO;2
WIND_SPEED_FORECAST = 3.75 # in ms^-1
WIND_SPEED_SIGMA = 0.4*WIND_SPEED_FORECAST
WIND_DIRECTION_FORECAST = 270 # in degrees
WIND_DIRECTION_SIGMA = (0.32/WIND_SPEED_FORECAST)*(180/np.pi)
NUMBER_OBSERVATIONS = 25
DATASET_SIZES = [2,10,25]
NUMBER_LOADLEVELS = 10

# Function to create a folder if it doesn't exist
def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)

# Function to generate .txt files using TXTfromCSV class
def generate_txt_file(output_folder, input_file):
    customers, distances = txtfromcsv.csvImporter(input_file)
    
    for size in DATASET_SIZES:
        print(f"Doing observation size {size}")
        travel_time_matrix = txtfromcsv.computeTravelTimeMatrix(customers, distances, 
                                                                WIND_SPEED_FORECAST, WIND_SPEED_SIGMA, WIND_DIRECTION_FORECAST, WIND_DIRECTION_SIGMA, 
                                                                size, NUMBER_LOADLEVELS)
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + f"_{size}.txt")
        txtfromcsv.write_travel_time_matrix_to_file(travel_time_matrix, len(customers), NUMBER_LOADLEVELS, size, output_file)
        
    
def generate_txt_files_from_folder(output_folder, input_folder):
    create_folder(output_folder)
    for root, _, files in os.walk(input_folder):
        for file in files:
            print(f"Busy converting {file}")
            input_file = os.path.join(root, file)
            generate_txt_file(output_folder, input_file)

def main():
    output_folder = "/Users/stijnvanderwal/Documents/GitHub/Simulator/Tests19mrt"
    input_folder = "/Users/stijnvanderwal/Documents/GitHub/SA-ILP_new/instances"
    generate_txt_files_from_folder(output_folder, input_folder)

if __name__ == "__main__":
    main()
