# -*- coding: utf-8 -*-
"""
Example script for Application 2. Reproduces the curves and data points of 
Figure 2b.
"""

import numpy as np
import pandas as pd
from StartPowerGUI import powerThread
from matplotlib import pyplot as plt

        
def main():
    """ Reproduces the curves and data points of Figure 2b."""
   
    # read input file for application 2
    df = pd.read_excel("Input_Application2.xlsx")            
    params = np.array(df.iloc[:,1:6])
    
    # define other parameters
    dose = np.array([0,20,30,40,50,60,70,80,90,100,120])
    k = 10000
    alpha = 0.05
    seed = 17
    N = 21
        
    print("Please be patient ...")
    print("---------------------")

    # generate instance of class
    pT = powerThread(N, k, dose, params, alpha, seed)
    # calculate power for N
    saveIndAr = pT.simulation(N, k, dose, params, alpha, seed, saveInd=True)

    # print resulting power   
    print("Control arm \t \t \t \t Experimental arm \t \t \t \t DMF \t \t \t \t Power")
    print("Median beta_0: {0:8.4f} \t Median beta_0: {1:8.4f} \t \t Median: {2:8.4f}\t{3:7.3f}".format(pT.results[0], pT.results[3], pT.results[6], pT.results[7]))
    print("Median beta_1: {0:8.4f} \t Median beta_1: {1:8.4f}".format(pT.results[1], pT.results[4]))
    print("Median TCD50:  {0:5.1f} Gy \t Median TCD50: \t {1:5.1f} Gy".format(pT.results[2], pT.results[5]))             
      
    # sort all simulated doses and events according to control and 
    # experimental arms
    grp = saveIndAr[:,2]
    dcont = saveIndAr[grp==0,0] 
    econt = saveIndAr[grp==0,1]
    dexp = saveIndAr[grp==1,0]
    eexp = saveIndAr[grp==1,1]
    # sort with increasing dose
    dindc = np.argsort(dcont)
    econt = econt[dindc]
    dinde = np.argsort(dexp)
    eexp = eexp[dinde]
    
    # calculate tumour-control fractions for both arms
    Nd = len(dose)
    tcfc = np.zeros(Nd)
    tcfe = np.zeros(Nd)
    for i in range(Nd):
        tcfc[i] = np.mean(econt[i*k*N:(i+1)*k*N])
        tcfe[i] = np.mean(eexp[i*k*N:(i+1)*k*N])
    
    # calculate median tcp prediction for both arms
    doseplot = np.linspace(0, 150, 400)
    tcpc = pT.logReg1(doseplot, pT.results[0], pT.results[1])
    tcpe = pT.logReg1(doseplot, pT.results[3], pT.results[4])

    # plot tcf and tcp values
    plt.plot(dose, tcfc, "ob")
    plt.plot(dose, tcfe, "or")
    plt.plot(doseplot, tcpc, "-b")
    plt.plot(doseplot, tcpe, "-r")
    plt.show()


if __name__ == '__main__':
    main()

