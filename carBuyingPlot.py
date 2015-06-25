import matplotlib.pyplot as plt
from matplotlib.backends import qt4_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import cPickle
from PyQt4 import QtGui, QtCore

# Custom modules/functions
import CarBuyingBackend as backend

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = plt.Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.ax.hold(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class carBuyingPlot(MyMplCanvas):
    def __init__(self, name = 'Name', parent = None):
        super(carBuyingPlot, self).__init__(parent=parent)
        self.name = name
        self.curves = {}

    def addCurve(self, min, max, avg, name = None, color = 'b'):
        self.curves[name] = Curve(min, max, avg, self.ax, color = color)
        return

    def addLegend(self):
        lines = []
        labels = []
        for label in self.curves.keys():
            lines.append(self.curves[label].avg)
            labels.append(label)
        self.legend = self.fig.legend(lines, labels, 'upper right')
        return

class Curve(object):
    def __init__(self, min, max, avg, ax, color = 'b', label = None, alpha = 0.2):
        self.bounds = self.getBounds(min, max, ax)
        self.avg = self.getAvg(avg, ax, label)
        self.bounds.set_alpha(0.2)
        self.setColor(color)
        self.setLabel(label)
        self.setAlpha(alpha)
        
    def getBounds(self, min, max, ax):
        x_values = min[:,0]
        bounds = plt.fill_between(x_values, min[:,1], max[:,1], axes = ax)
        return bounds

    def getAvg(self, avg, ax, label):
        x_values = avg[:,0]
        #avgPlot = plt.Line2D(x_values, avg[:,1], axes = ax, linewidth = 2)
        avgPlot, = plt.plot(x_values, avg[:,1], axes = ax)
        return avgPlot

    def setColor(self, color):
        self._color = color
        self.bounds.set_facecolors(color)
        self.avg.set_color(color)
        return

    def setAlpha(self, alpha):
        self._alpha = alpha
        self.bounds.set_alpha(alpha)
        return

    def updateValues(self, min, max, avg, ax):
        x_values = min[:,0]
        self.bounds = plt.fill_between(x_values, min[:,1], max[:,1], axes = ax, alpha = self._alpha, color = self._color)
        return

    def setLabel(self, label):
        self.avg.set_label(label)
        return

def getTestData(year = '2011'):
    data = backend.getMakeData('Toyota')
    return data.data['Prius'][year]['One Hatchback 4D ']

def testAddData(years, plot, colors = ['r', 'g', 'b']):
    for i, year in enumerate(years):
        data = getTestData(year = str(year))

        min = data['priceMin']
        max = data['priceMax']
        avg = data['price']
        plot.addCurve(min, max, avg, name = str(year), color = colors[i])

    plot.addLegend()
    return

if __name__ == '__main__':
    import numpy as np

    plot = carBuyingPlot()
    years = [2011, 2013]#, 2013]
    
    testAddData(years, plot)
    plt.show()