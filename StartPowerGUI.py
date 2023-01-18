# -*- coding: utf-8 -*-
"""
Sample size calculation for two-arm 1:1 comparative dose-response studies.
@authors: Willy Ciecior, Steffen Löck
License: GPLv3
"""

import sys
import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from defGUI import Ui_Dialog
from PyQt5 import QtWidgets, QtCore


class GUI(QtWidgets.QWidget, Ui_Dialog):
    """ 
    Class containing the GUI and calling the power calculation method     
    """       
    def __init__(self, parent = None):
        """ 
        Constructor: setup GUI and link buttons
        """        
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)      
        
        # set default values
        self.alpha = 0.05                           # significance level
        self.N = 10                                 # number of animals per dose group
        self.k = 1000                               # number of repetitions
        self.dose = [30,40,50,60,72.5,80,100]       # dose lavels
        self.filename = "DEFAULT CASE"              # no file selected
        self.params = np.array([[-7.188,0.115,1.25,1,1]])  # FaDu as default
        self.seed = 17                           # initial seed
        
        # Set default parameters in line edits
        self.lineEditAlpha.setText("{0:1.2f}".format(self.alpha))
        self.lineEditSeed.setText("{0:d}".format(self.seed))
        self.lineEditN.setText("{0:d}".format(self.N))
        self.lineEditK.setText("{0:d}".format(self.k))
        doselevel = ', '.join([str(elem) for elem in self.dose])        
        self.textEditDose.setText(doselevel)
        self.lineEditFile.setText(self.filename)
               
        # link buttons to methods
        self.pushButtonCalculate.clicked.connect(self.startCalculation)
        self.pushButtonOpen.clicked.connect(self.openFile)
        self.pushButtonClose.clicked.connect(self.close)
        self.pushButtonUpdate.clicked.connect(self.updateParams)
        
        # set labels and default values for dose-response plot 
        self.widgetPlot.canvas.axes.set_xlabel(r"Dose [Gy]")
        self.widgetPlot.canvas.axes.set_ylabel(r"TCP")
        self.widgetPlot.canvas.axes.grid(True)
        self.lineEditXMin.setText("0")
        self.lineEditXMax.setText("150")
        self.lineEditGrid.setText("200")        
        self.XMin = float(self.lineEditXMin.text())
        self.XMax = float(self.lineEditXMax.text())
        self.Grid = float(self.lineEditGrid.text())               
        
    def updateParams(self):
        """ Updates parameters and plot settings"""       
        # read parameters from edits
        self.XMin = float(self.lineEditXMin.text())
        self.XMax = float(self.lineEditXMax.text())
        self.Grid = int(self.lineEditGrid.text())       
        self.alpha = float(self.lineEditAlpha.text())
        self.N = int(self.lineEditN.text())
        self.k = int(self.lineEditK.text())   
        self.seed = int(self.lineEditSeed.text()) 
        dose = self.textEditDose.toPlainText()
        self.dose = np.asarray((str(dose)).split(","), dtype=np.float64)
        # update plot          
        self.widgetPlot.canvas.axes.set_xlim(self.XMin,self.XMax)
        self.widgetPlot.canvas.draw() 
        # append status to status edit
        self.textEdit.append("Input parameters updated")  
            
    def openFile(self):       
        """
        Select an .xlsx file with the required parameters for power 
        calculation.
        """               
        # clear status edit
        self.textEdit.clear()
        # ope file dialog
        filename = QtWidgets.QFileDialog.getOpenFileName (filter = "Excel files (*.xlsx)")[0]
        # save filename and show in edit
        filename = str(filename)        
        if filename != "":
            self.filename = filename
            self.lineEditFile.setText(self.filename)
        else:
            self.lineEditFile.setText("canceled ...")     
                         
    def startCalculation(self):      
        """
        Prepares parameters for simulation, calls the simulation and shows
        results.        
        """
        # clear plot          
        self.widgetPlot.canvas.axes.clear()
        self.widgetPlot.canvas.draw()        
        
        # read parameters from edits
        self.alpha = float(self.lineEditAlpha.text())
        self.N = int(self.lineEditN.text())                    
        self.k = int(self.lineEditK.text())
        self.seed = int(self.lineEditSeed.text()) 
        dose = self.textEditDose.toPlainText()
        self.dose = np.asarray((str(dose)).split(","), dtype=np.float64)
        # stop if N<3 (often the model does not converge)
        if self.N < 3:
            self.textEdit.append("Number of animals per dose group should be larger than 2. Please increase.")
            return
        
        # load previously selected excel file and save content to self.params
        if self.filename != "DEFAULT CASE":
            df = pd.read_excel(self.filename)             
            self.params = np.array(df.iloc[:,1:6])                                 
            
        # start power calculation     
        self.thread = powerThread(self.N, self.k, self.dose, self.params, 
                                  self.alpha, self.seed)    
        self.pushButtonCalculate.setEnabled(False)
        self.thread.finished.connect(self.endCalculation)
        self.thread.sig.connect(self.progressBar)
        self.thread.start()   
        
    def progressBar(self, msg):
        """ Receives emitted string from thread """
        self.textEdit.setText("Progress: "+msg+"%")
        
    def endCalculation(self):
        """ Called after powerThread has finished """
        self.output = self.thread.results   
        self.pushButtonCalculate.setEnabled(True)
        
        # read plot details
        xMin = float(self.lineEditXMin.text())
        xMax = float(self.lineEditXMax.text())
        xGrid=int(self.lineEditGrid.text())
        # plot median dose-response curvs of both arms
        x = np.linspace(xMin, xMax, xGrid)
        y1 = self.thread.logReg1(x, self.output[0], self.output[1])
        y2 = self.thread.logReg1(x, self.output[3], self.output[4])
        self.widgetPlot.canvas.axes.clear()
        self.widgetPlot.canvas.axes.plot(x,y1,color = "navy", 
                                              label = "Control arm")
        self.widgetPlot.canvas.axes.plot(x,y2,color = "darkorange", 
                                              label = "Experimental arm")
        self.widgetPlot.canvas.axes.legend(loc=0)
        self.widgetPlot.canvas.axes.grid(True)
        self.widgetPlot.canvas.axes.set_xlabel(r"Dose [Gy]")
        self.widgetPlot.canvas.axes.set_ylabel(r"TCP")
        self.widgetPlot.canvas.draw()   
                
        # empty status edit and print results
        self.textEdit.clear()        
        self.textEdit.append("Control arm \t \t \t Experimental arm \t \t DMF \t \t  Power")
        self.textEdit.append("")
        self.textEdit.append("Median beta_0: {0:7.3f} \t \t Median beta_0: {1:7.3f} \t \t Median: {2:7.3f}\t\t{3:7.3f}".format(self.output[0], self.output[3], self.output[6], self.output[7]))
        self.textEdit.append("Median beta_1: {0:7.3f} \t \t Median beta_1: {1:7.3f}".format(self.output[1], self.output[4]))
        self.textEdit.append("Median TCD50:  {0:5.1f} Gy \t \t Median TCD50: \t {1:5.1f} Gy".format(self.output[2], self.output[5]))         
       

class powerThread(QtCore.QThread):
    """ Class for threaded power calculation """
    sig = QtCore.pyqtSignal(str)   # generate a signal for communication
    
    def __init__(self, N, k, dose, params, alpha, seed):
        """ Initialize thread """
        QtCore.QThread.__init__(self, parent=None)
        self.runs = True
        self.N = N
        self.k = k
        self.dose = dose
        self.params = params
        self.alpha = alpha
        self.seed = seed
        
    def run(self):
        """ Starts power calculation """
        self.simulation(self.N, self.k, self.dose, self.params, self.alpha,
                        self.seed) 
        
    def logReg1(self, x1, b0, b1):
        """ Logistic regression with one independent variable:
            x1: dose [e.g., in Gy]
            b0, b1: fit coefficients
        """         
        return 1/(1+np.exp(-b0-b1*x1))
    
    def logReg2(self, x1, x2, b0, b1, b2):
        """ Logistic regression with two independent variables:
            x1: dose [e.g., in Gy]
            x2: group [0 or 1]
            b0, b1, b2: fit coefficients
        """        
        return 1/(1+np.exp(-b0-b1*x1-b2*x2))    

    def simulation(self, N, k, dose, params, alpha, seed, saveInd=False):   
        """ 
        Power calculation function.
        N: Number of animals per dose group in one arm
        k: Number of random repetitions
        dose: Array of used dose values
        params: 2D array containing beta0, beta1, DMF, absolute and relative 
                frequency of cell lines (from .xlsx file) 
        alpha: Significance level        
        """     
        self.sig.emit("Calculation starting")
        # zero arrays for regression coefficients b0 and b1 and for the TCD50
        #  for arms A and B
        Ab0ar = np.zeros(k)
        Ab1ar = np.zeros(k)
        Bb0ar = np.zeros(k)
        Bb1ar = np.zeros(k)
        Atcd50 = np.zeros(k)
        Btcd50 = np.zeros(k)
        # arry for significant test results
        TR = np.zeros(k)    
        
        # calculate dose array (same for both arms A and B)
        Ndose = len(dose)
        ABdar = np.zeros(Ndose*N)
        for i in range(Ndose):
            ABdar[i*N:(i+1)*N] = dose[i]            
        # calculate concatenated dose array for both arms and reshape
        Cdar = np.concatenate((ABdar, ABdar), axis=None)
        Cdar = Cdar.reshape(-1,1)
        # rescale the dose to [0,1] because the fast saga solver requires it
        Dmin, Dmax = np.min(dose), np.max(dose)
        Cdar = (Cdar-Dmin)/(Dmax-Dmin)
        
        # create array for arm membership and reshape
        Cgar = np.zeros(2*Ndose*N, dtype=np.int32)
        Cgar[Ndose*N:] = 1 
        Cgar = Cgar.reshape(-1,1)
        
        # create logistic model
        LRmodel = LogisticRegression(penalty='none', solver='saga', 
                                     max_iter=5000, tol=1e-4)
            
        # shortcuts
        Nx = params.shape[0]
        N_ = N*Ndose
        
        # set seed
        np.random.seed(seed)
        
        # if saveInd is True: save all simulated (dose,event,group) pairs
        if saveInd:
            saveIndAr = np.zeros((2*Ndose*N*k,3))
        else:
            saveIndAr = None
        
        # Repeat simulation k times
        for i in range(k):
            # emit progress in steps of 5%
            prog = i/k
            if (i/k*100)%5 < 1 and ((i-1)/k*100)%5 > 4:
                self.sig.emit(str(int(prog*100)))
                                       
            # Arm A
            # randomly select N*Ndose xenografts
            Arandx = np.random.choice(Nx, N_, replace=True, p=params[:, 4])
            # calculate TCP of individual xenografts at dose values
            params_ = params[Arandx,:]
            Atcp = self.logReg1(ABdar, params_[:,0], params_[:,1])
            # draw N*Nd uniform random numbers between 0 and 1
            Au = np.random.uniform(0, 1, N*Ndose)
            # set event if random number smaller than TCP
            Aear = np.int32(Au<Atcp) 
            
            # Arm B
            # randomly select N*Ndose xenografts
            Brandx = np.random.choice(Nx, N_, replace=True, p=params[:, 4])
            # calculate TCP of individual xenografts at dose values
            params_ = params[Brandx,:]
            Btcp = self.logReg1(ABdar, params_[:,0]/params_[:,2], 
                                params_[:,1])
            # draw N*Nd uniform random numbers between 0 and 1
            Bu = np.random.uniform(0, 1, N*Ndose)
            # set event if random number smaller than TCP
            Bear = np.int32(Bu<Btcp)
         
            # concatenate event arrays
            Cear = np.concatenate((Aear, Bear), axis=None)           
            # hstack for logistic regression
            Ccar = np.hstack([Cdar, Cgar]) 
            
            # if saveInd is True: save all simulated (dose,event,group) pairs
            if saveInd:
                saveIndAr[2*Ndose*N*i:2*Ndose*N*(i+1),0] = np.ravel(Cdar) 
                saveIndAr[2*Ndose*N*i:2*Ndose*N*(i+1),1] = np.ravel(Cear)
                saveIndAr[2*Ndose*N*i:2*Ndose*N*(i+1),2] = np.ravel(Cgar)
            
            # fit logistic regression with independent parameter dose,
            #  calculate predicted probabilities and log-likelihood
            RMclf = LRmodel.fit(Cdar, Cear)
            Y_RM = RMclf.predict_proba(Cdar)[:,1]
            LLRM = -log_loss(Cear, Y_RM)*len(Y_RM)
            
            # fit logistic regression with independent parameters dose and arm,
            #  calculate predicted probabilities and log-likelihood
            UMclf = LRmodel.fit(Ccar, Cear)
            Y_UM = UMclf.predict_proba(Ccar)[:,1] 
            LLUM = -log_loss(Cear, Y_UM)*len(Y_UM)            
                                                
            # rescale fit coefficients to dose scale in real units (Gy)
            b0 = UMclf.intercept_-UMclf.coef_[:, 0]*Dmin/(Dmax-Dmin)
            b1 = UMclf.coef_[:, 0]/(Dmax-Dmin)
            b2 = UMclf.coef_[:, 1]
            # save fit coefficients for both arms in arrays
            Ab0ar[i] = b0
            Ab1ar[i] = b1
            Bb0ar[i] = b0 + b2
            Bb1ar[i] = b1
            
            # calculate likelihood ratio for testing
            LR = -2*(LLRM-LLUM)
            # p-value of the likelihood-ratio test
            p = 1 - chi2.cdf(LR, 1)
            # if p-value smaller than significance level: test result positive
            TR[i] = np.int32(p < alpha)
            # compare tcd50 between control and experimental arm.
            #  if tcd50 of the control arm is smaller than of the experimental
            #  arm: set test result to negative (0)
            Atcd50[i] = -Ab0ar[i]/Ab1ar[i]
            Btcd50[i] = -Bb0ar[i]/Bb1ar[i]
            if Atcd50[i] <= Btcd50[i]:
                TR[i] = 0
                
        # calculate median fit coefficients and tcd50 per arm for 
        #  visualization and as additional output
        Ab0median = np.median(Ab0ar)
        Ab1median = np.median(Ab1ar)
        Atcd50median = np.median(Atcd50)
        Bb0median = np.median(Bb0ar)
        Bb1median = np.median(Bb1ar)
        Btcd50median = np.median(Btcd50)
        # calculate median dose modification factor
        DMF = np.median(Atcd50 / Btcd50)
        # calculate power
        power = np.sum(TR)/k               
        # compile a list of results for visualization
        self.results = [Ab0median, Ab1median,  Atcd50median,
                        Bb0median, Bb1median,  Btcd50median,
                        DMF, power] 
        # signal end of calculation
        self.sig.emit("Calculation finished")        
        return saveIndAr

    def stop(self): 
        """ Can be used to stop the calculation """
        self.runs = False    
        self.sig.emit("Calculation aborted")
                 
         
def main():
    """ Start GUI """
    app = QtWidgets.QApplication(sys.argv)
    powdrc = GUI()    
    powdrc.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

