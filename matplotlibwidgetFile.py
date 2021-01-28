"""
Given a QWidget object these objects give a matplotlib window in Qt5
with one subplot and the toolbar. 
"""

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
 
from matplotlib.figure import Figure
 
 
class MplCanvas(FigureCanvas):
    """
    Defines the canvas of the matplotlib window
    """
    def __init__(self):
        self.fig = Figure()                         # create figure
        self.axes = self.fig.add_subplot(111)       # create subplot
        
        FigureCanvas.__init__(self, self.fig)       # initialize canvas
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
 
class matplotlibWidget(QtWidgets.QWidget):
    """
    The matplotlibWidget class based on QWidget
    """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # save canvas and toolbar
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)        
        # set layout and add them to widget
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)
