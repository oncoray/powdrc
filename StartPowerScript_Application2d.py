# -*- coding: utf-8 -*-
"""
Example script for Application 2. Reproduces the modified
power curve of Figure 2d.
"""

import numpy as np
import pandas as pd
from StartPowerGUI import powerThread

        
def main():
    """ Calculate and print power for Application 2 for N=2 to N=40
        with modified dose levels."""
   
    # read input file for application 1
    df = pd.read_excel("Input_Application2.xlsx")            
    params = np.array(df.iloc[:,1:6])
    
    # define other parameters
    dose = np.array([20,25,30,35,40,45,50,60,70,85,100])
    k = 10000
    alpha = 0.05
    seed = 17
    Nar = np.arange(2, 41, 1)
    pwar = []
        
    print("Please be patient ...")
    print("---------------------")
    for N in Nar:
        # generate instance of class
        pT = powerThread(N, k, dose, params, alpha, seed)
        # calculate power for N
        pT.simulation(N, k, dose, params, alpha, seed)
        # here is the power
        power = pT.results[-1]
        pwar.append(power)
        # print resulting power               
        print("N: {0:d} \t \t Power: {1:7.3f}".format(N, power))       
        print(pwar)

if __name__ == '__main__':
    main()

