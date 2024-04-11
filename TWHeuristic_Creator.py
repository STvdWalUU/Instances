#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 10:29:22 2024

@author: stijnvanderwal

This file is used to create instances that can be used in the heuristic of 
adapted time windows
"""

"""imports"""
import csv

"""universal variables"""
filename = "/Users/stijnvanderwal/Documents/GitHub/Simulator/CSVfiles_full/Utrecht_full.csv"

"""function definitions"""
def AdjustLine(line, AdjustmentType):
    if AdjustmentType == "min15m":
        NewTimeWindowEnd = str(max(float(line[6])-15,0))
    elif AdjustmentType == "min10pc":
        NewTimeWindowEnd = str(max(float(line[6])-0.1*(float(line[6])-float(line[5])),0))
    else:
        raise Exception("AdjustmentType is incorrect. \n choose from: min15m, min10pc.")
        
    return NewTimeWindowEnd

""" Deze functie laadt de instance die aangepast moet worden"""
def ReadCSVfile(filename):
    print("Reading the original instance..")
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        outputLines = []
        first_line = next(csv_reader)
        
        outputLines.append(first_line)
    
        for line in csv_reader:
            outputLines.append(line)
                
    return outputLines

def AdjustLines(OldLines):
    print("Adjusting data..")
    
    for line in OldLines[2:]:
        #print(f"old: {line[6]}")
        line[6] = AdjustLine(line, AdjustmentType = "min15m")
        #print(f" new:{line[6]}")
    return OldLines

def WritingToCSVfile(NewLines):
    print("Writing new Instance to csv..")
    with open(filename.replace(".csv", "")+"_NewTW.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(NewLines)
    
def main():
    OldLines = ReadCSVfile(filename)
    NewLines = AdjustLines(OldLines)
    WritingToCSVfile(NewLines)
    
if __name__ == '__main__':
    main()