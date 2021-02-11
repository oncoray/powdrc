# -*- coding: utf-8 -*-
"""
Example script for Application 1. Reproduces Figure 1c.
"""

import numpy as np
import pandas as pd
from StartPowerGUI import powerThread

        
def main():
    """ Calculate and print power for Application 1 (FaDu) in dependence of the
        dose-modifying factor."""
   
    # read input file for application 1
    df = pd.read_excel("Input_Application1.xlsx")            
    params = np.array(df.iloc[:,1:6])
    
    # define other parameters
    dose = np.array([30,40,50,60,72.5,80,100])
    k = 10000
    alpha = 0.05
    seed = 17
    Nar = np.arange(1, 70, 1)
    
    print("Please be patient ...")
    print("---------------------")
    for dmf in np.linspace(1.1,2.0,19):
        print("-----")
        print("-----")
        print("DMF=",dmf)
        print("-----")
        params[0][2] = dmf
        for N in Nar:
            if dmf < 1.14 and N < 45: continue
            if dmf < 1.19 and N < 20: continue
            if dmf < 1.24 and N < 12: continue
            if dmf < 1.29 and N < 8: continue
                
            # generate instance of class
            pT = powerThread(N, k, dose, params, alpha, seed)
            # calculate power for N
            pT.simulation(N, k, dose, params, alpha, seed)
            # here is the power
            power = pT.results[-1]
            # print resulting power               
            print("N: {0:d} \t \t Power: {1:7.3f}".format(N, power))  
            if power > 0.85:
                break
          

if __name__ == '__main__':
    main()

