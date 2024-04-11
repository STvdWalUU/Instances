#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 15:02:13 2024

@author: stijnvanderwal

This file is meant for creating a TXT file with only one 'observation'
This observation is the expected value of the travel time after simulating it 
some number of times.
"""

import os
import txtfromcsv
import numpy as np
import random
import math

random.seed(43)

# Constants
# Values rectified by https://doi.org/10.1175/1520-0450(1988)027%3C0550:SDOWSA%3E2.0.CO;2
WIND_SPEED_FORECAST = 3.75 # in ms^-1
WIND_SPEED_SIGMA = 0.4*WIND_SPEED_FORECAST
WIND_DIRECTION_FORECAST = 0 # in degrees
WIND_DIRECTION_SIGMA = (0.32/WIND_SPEED_FORECAST)*(180/np.pi)
NUMBER_OBSERVATIONS = 1
NUMBER_LOADLEVELS = 10

# Function to create a folder if it doesn't exist
def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    
def computeExpectedTravelTimeMatrix(customers, distance_matrix, wind_speed_forecast, wind_speed_sigma, wind_direction_forecast, wind_direction_sigma, number_observations, number_loadlevels):
    """
    This function will return a 'flattened' matrix (in 2D) that can be exported 
    using .TXT and understood by the C# algorith for SA-ILP. It takes in a
    predefined list of customers and a distance matrix. These, together with
    generated wind forecasts (Monte-Carle like), determine the 'observations'
    for the travel time between each pair of customers and each possible loadlevel.
    """
    try:
        scale = wind_speed_sigma**2 / wind_speed_forecast
        shape = wind_speed_forecast / scale
    except ZeroDivisionError:
        shape = 0
    
    nr_edges = len(customers)**2
    nr_columns = number_loadlevels
    travel_time_matrix = np.zeros((nr_edges, nr_columns))
    
    for n in range(nr_columns):
        if shape == 0:
            wind_speed = wind_speed_forecast
        else:
            wind_speed = max(0, random.gammavariate(shape, scale))
        wind_direction = random.normalvariate(wind_direction_forecast, wind_direction_sigma)
        
        load_level = n
        
        for cust_start, start_customer in enumerate(customers):
            for cust_end, end_customer in enumerate(customers):
                if cust_start != cust_end:
                    travel_distance = distance_matrix[cust_start, cust_end]
                    heading = math.atan2((end_customer.y - start_customer.y), (end_customer.x - start_customer.x))
                    wind_angle = wind_direction - heading
                    slope = (end_customer.h - start_customer.h) / travel_distance
                    travel_time_list = []
                    for i in range(number_observations):
                        travel_time_list.append(txtfromcsv.TravelTimeComputer(load_level, number_loadlevels,travel_distance, slope, wind_speed, wind_angle))
                    expected_travel_time = np.average(travel_time_list)
                    travel_time_matrix[cust_start * len(customers) + cust_end, n] = round(expected_travel_time, 2)
            print(n, cust_start * len(customers) + cust_end)
    return travel_time_matrix
# Function to generate .txt files using TXTfromCSV class
def generate_txt_file(output_folder, input_file):
    customers, distances = txtfromcsv.csvImporter(input_file)
    travel_time_matrix = computeExpectedTravelTimeMatrix(customers, distances, 
                                                            WIND_SPEED_FORECAST, WIND_SPEED_SIGMA, WIND_DIRECTION_FORECAST, WIND_DIRECTION_SIGMA, 
                                                            NUMBER_OBSERVATIONS, NUMBER_LOADLEVELS)
    output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + f"_Ws{WIND_SPEED_FORECAST}_Wd{WIND_DIRECTION_FORECAST}_ETT{NUMBER_OBSERVATIONS}_0.txt")
    txtfromcsv.write_travel_time_matrix_to_file(travel_time_matrix, len(customers), 
                                                NUMBER_LOADLEVELS, "ETT", output_file, 
                                                WIND_SPEED_FORECAST, WIND_DIRECTION_FORECAST)
    
def generate_txt_files_from_folder(output_folder, input_folder):
    create_folder(output_folder)
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith("Store"):
                continue
            if file.endswith("utrecht_full.csv"):
                print(f"Busy converting {file}")
                input_file = os.path.join(root, file)
                generate_txt_file(output_folder, input_file)

def main():
    output_folder = "/Users/stijnvanderwal/Documents/GitHub/Simulator/TXTilesFull_ETT"
    input_folder = "/Users/stijnvanderwal/Documents/GitHub/Simulator/CSVfilesFull"
    generate_txt_files_from_folder(output_folder, input_folder)

if __name__ == "__main__":
    main()