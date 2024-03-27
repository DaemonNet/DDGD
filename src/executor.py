#################################################################################################################
# Author: Alexander Diedrich
# Initial Date: 05.05.2022
# Updated: 27.03.2024
# Description: Main file to run experiments. All generated files will be written into folder "output".
# Each step generates its own files, which are plaintext and can be inspected. This file performs correlation
# and Granger Causality analysis, and executes diagnosis on simulated (random observations are set to faulty)
# and real fault data (taken from the input process data). 
# NOTE: COMPS.csv must be filled out. Unused Granger and Correlation files can be commented out. 
# All files in "output" folder are generated automatically
#################################################################################################################

import random

#Granger
import granger_Tanks as g_tanks
import granger_TenneseeEastman as g_te
import granger_Tanks_absolute as g_tanks_abs

#Correlation
import correlation_Simu as corr_Simu
import correlation_IGV as corr_IGV

#Diagnosis

from manualDiagEval import ManualExecution
from diagExecution import *



def runGranger():

    print("Running tanks data")
    path = "..\\data\\tanks"
    g_tanks.run_TanksSimulations(path)

    print("Running tanks from Jonas Ehrhardt data")
    path = "..\\data\\jonasTanks"
    g_tanks.run_TanksSimulations(path)

    print("Running Granger with absolute values Simu")
    path = "..\\data\\tanks"
    g_tanks_abs.run_grangerAbsoluteSimu(path) 

    print("Running TE data")
    path = "../data/1_Tests/"
    g_te.run_TESimulation(path, False)


if __name__ == '__main__': 
    random.seed(1337)
    logfile = open("output/diag.log", "w")

    #Perform Granger Causality analysis and generate files accordingly
    runGranger()   
    
    logfile.close()