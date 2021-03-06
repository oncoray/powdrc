# -*- coding: utf-8 -*-
"""
Example script for Application 1. Reproduces the power curve of Figure 1b.
"""

import numpy as np
import pandas as pd
from StartPowerGUI import powerThread

        
def main():
    """ Calculate and print power for Application 1 (FaDu) for N=2 to N=20."""
   
    # read input file for application 1
    df = pd.read_excel("Input_Application1.xlsx")            
    params = np.array(df.iloc[:,1:6])
    
    # define other parameters
    dose = np.array([30,40,50,60,72.5,80,100])
    k = 10000
    alpha = 0.05
    seed = 17
    Nar = np.arange(2, 21, 1)
        
    print("Please be patient ...")
    print("---------------------")
    for N in Nar:
        # generate instance of class
        pT = powerThread(N, k, dose, params, alpha, seed)
        # calculate power for N
        pT.simulation(N, k, dose, params, alpha, seed)
        # here is the power
        power = pT.results[-1]
        # print resulting power               
        print("N: {0:d} \t \t Power: {1:7.3f}".format(N, power))       
          

if __name__ == '__main__':
    main()

