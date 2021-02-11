# -*- coding: utf-8 -*-
"""
Example script for Application 2. Reproduces the modified 
power curve of Figure 2f.
"""

import numpy as np
import pandas as pd
from StartPowerGUI import powerThread

        
def main():
    """ Calculate and print power for Application 2 in dependence of the
        dose-modifying factor."""
   
    # read input file for application 2
    df = pd.read_excel("Input_Application2.xlsx")            
    params = np.array(df.iloc[:,1:6])
    
    # define other parameters
    dose = np.array([0,20,30,40,50,60,70,80,90,100,120])
    k = 10000
    alpha = 0.05
    seed = 17
    Nlb = [96,48,26,18,14,12,8,6,4,1,1,1,1,1,1,1,1,1,1]
    
        
    print("Please be patient ...")
    print("---------------------")
    for i, dmf in enumerate(np.linspace(1.1,2.0,19)):
        Nar = np.arange(Nlb[i], 220, 1)
        print("-----")
        print("-----")
        print("DMF=",dmf)
        print("-----")
        
        params[:,2] = dmf
        for N in Nar:
            # generate instance of class
            pT = powerThread(N, k, dose, params, alpha, seed)
            # calculate power for N
            pT.simulation(N, k, dose, params, alpha, seed)
            # here is the power
            power = pT.results[-1]
            # print resulting power  
            if power > 0.85: break
            if power > 0.7: 
                print("N: {0:d} \t \t Power: {1:7.3f}".format(N, power))       
          

if __name__ == '__main__':
    main()

