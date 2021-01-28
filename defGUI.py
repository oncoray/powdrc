# -*- coding: utf-8 -*-
"""
Definitions for the GUI
"""

from PyQt5 import QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1133, 742)
                        
        # Matplotwidget
        self.widgetPlot = matplotlibWidget(Dialog)
        self.widgetPlot.setGeometry(QtCore.QRect(210, 30, 791, 481))
        self.widgetPlot.setObjectName(_fromUtf8("widgetPlot"))
        
        # Buttons
        self.pushButtonOpen = QtWidgets.QPushButton(Dialog)
        self.pushButtonOpen.setGeometry(QtCore.QRect(680, 650, 101, 23))
        self.pushButtonOpen.setObjectName(_fromUtf8("pushButtonOpen"))       
        self.pushButtonCalculate = QtWidgets.QPushButton(Dialog)
        self.pushButtonCalculate.setGeometry(QtCore.QRect(790, 650, 101, 23))
        self.pushButtonCalculate.setObjectName(_fromUtf8("pushButtonCalculate"))        
        self.pushButtonClose = QtWidgets.QPushButton(Dialog)
        self.pushButtonClose.setGeometry(QtCore.QRect(900, 650, 101, 23))
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))        
        self.pushButtonUpdate = QtWidgets.QPushButton(Dialog)
        self.pushButtonUpdate.setGeometry(QtCore.QRect(20, 500, 75, 23))
        self.pushButtonUpdate.setObjectName(_fromUtf8("pushButtonUpdate"))
                
        # LineEdits, Textedits + Labels Eingabe       
        self.labelSeed = QtWidgets.QLabel(Dialog)
        self.labelSeed.setGeometry(QtCore.QRect(20, 50, 111, 16))
        self.labelSeed.setObjectName(_fromUtf8("labelSeed"))
        self.lineEditSeed = QtWidgets.QLineEdit(Dialog)
        self.lineEditSeed.setGeometry(QtCore.QRect(20, 70, 111, 20))
        self.lineEditSeed.setText(_fromUtf8(""))
        self.lineEditSeed.setObjectName(_fromUtf8("lineEditSeed")) 
            
        self.labelAlpha = QtWidgets.QLabel(Dialog)
        self.labelAlpha.setGeometry(QtCore.QRect(20, 150, 111, 16))
        self.labelAlpha.setObjectName(_fromUtf8("labelAlpha"))
        self.lineEditAlpha = QtWidgets.QLineEdit(Dialog)
        self.lineEditAlpha.setGeometry(QtCore.QRect(20, 170, 111, 20))
        self.lineEditAlpha.setText(_fromUtf8(""))
        self.lineEditAlpha.setObjectName(_fromUtf8("lineEditAlpha"))          
        
        self.labelK = QtWidgets.QLabel(Dialog)
        self.labelK.setGeometry(QtCore.QRect(20, 200, 111, 16))
        self.labelK.setObjectName(_fromUtf8("labelL"))
        self.lineEditK = QtWidgets.QLineEdit(Dialog)
        self.lineEditK.setGeometry(QtCore.QRect(20, 220, 111, 20))
        self.lineEditK.setText(_fromUtf8(""))
        self.lineEditK.setObjectName(_fromUtf8("lineEditK"))
               
        self.labelN = QtWidgets.QLabel(Dialog)
        self.labelN.setGeometry(QtCore.QRect(20, 250, 151, 16))
        self.labelN.setObjectName(_fromUtf8("labelN"))
        self.lineEditN = QtWidgets.QLineEdit(Dialog)
        self.lineEditN.setGeometry(QtCore.QRect(20, 270, 111, 20))
        self.lineEditN.setText(_fromUtf8(""))
        self.lineEditN.setObjectName(_fromUtf8("lineEditN"))      
        
        self.labelDose = QtWidgets.QLabel(Dialog)
        self.labelDose.setGeometry(QtCore.QRect(20, 300, 111, 16))
        self.labelDose.setObjectName(_fromUtf8("labelDose"))       
        self.textEditDose = QtWidgets.QTextEdit(Dialog)
        self.textEditDose.setGeometry(QtCore.QRect(20, 320, 111, 60))
        self.textEditDose.setObjectName(_fromUtf8("textEditDose"))
        
        self.lineEditFile = QtWidgets.QLineEdit(Dialog)
        self.lineEditFile.setGeometry(QtCore.QRect(680, 680, 321, 20))
        self.lineEditFile.setText(_fromUtf8(""))
        self.lineEditFile.setReadOnly(True)
        self.lineEditFile.setObjectName(_fromUtf8("lineEditFile"))  
     
        # TextEdit Ausgabe
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setEnabled(True)
        self.textEdit.setGeometry(QtCore.QRect(210, 520, 791, 111))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))                         
        
        # Widgets Ploteigenschaften
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 410, 111, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEditXMin = QtWidgets.QLineEdit(Dialog)
        self.lineEditXMin.setGeometry(QtCore.QRect(20, 430, 51, 20))
        self.lineEditXMin.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEditXMin.setObjectName(_fromUtf8("lineEditXMin"))
        self.lineEditXMax = QtWidgets.QLineEdit(Dialog)
        self.lineEditXMax.setGeometry(QtCore.QRect(80, 430, 51, 20))
        self.lineEditXMax.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEditXMax.setObjectName(_fromUtf8("lineEditXMax"))
        self.lineEditGrid = QtWidgets.QLineEdit(Dialog)
        self.lineEditGrid.setGeometry(QtCore.QRect(20, 460, 111, 20))
        self.lineEditGrid.setObjectName(_fromUtf8("lineEditGrid"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Power Calculation for Dose-Response Curves", "Power Calculation for Dose-Response Curves", None))
       
        self.pushButtonOpen.setToolTip(_translate("Dialog", "<html><head/><body><p>Open parameter file (.xlsx)</p></body></html>", None))
        self.pushButtonOpen.setText(_translate("Dialog", "Open file", None))             
        self.pushButtonCalculate.setToolTip(_translate("Dialog", "<html><head/><body><p>Start power calculation using the given parameters</p></body></html>", None))
        self.pushButtonCalculate.setText(_translate("Dialog", "Calculate power", None))                
        self.pushButtonClose.setToolTip(_translate("Dialog", "<html><head/><body><p>Close the program</p></body></html>", None))
        self.pushButtonClose.setText(_translate("Dialog", "Close", None))               
        self.labelAlpha.setToolTip(_translate("Dialog", "<html><head/><body><p>Set significance level alpha (e.g. 0.05)</p></body></html>", None))
        self.labelAlpha.setText(_translate("Dialog", "Significance level", None))    
        self.labelSeed.setToolTip(_translate("Dialog", "<html><head/><body><p>Set the seed for the random number generator</p></body></html>", None))
        self.labelSeed.setText(_translate("Dialog", "Set seed", None))                 
        self.labelK.setToolTip(_translate("Dialog", "<html><head/><body><p>Set number of repetitions (should be >=1000, best 10000)</p></body></html>", None))
        self.labelK.setText(_translate("Dialog", "Repetitions", None))                             
        self.labelN.setToolTip(_translate("Dialog", "<html><head/><body><p>Number of animals per dose level per arm</p></body></html>", None))
        self.labelN.setText(_translate("Dialog", "Animal number per dose level", None))                
        self.labelDose.setToolTip(_translate("Dialog", "<html><head/><body><p>Set dose levels (comma separated)</p></body></html>", None))
        self.labelDose.setText(_translate("Dialog", "Dose levels", None))               
        self.pushButtonUpdate.setText(_translate("Dialog", "Update", None))        
        self.label.setToolTip(_translate("Dialog", "<html><head/><body><p>Upper line: minimal and maximal dose for plotting </p><p>Lower line: number of grid points for plot</p></body></html>", None))
        self.label.setText(_translate("Dialog", "Plot parameters", None))

from matplotlibwidgetFile import matplotlibWidget
