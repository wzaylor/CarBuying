import matplotlib.pyplot as plt
from matplotlib.backends import qt4_compat
#use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import cPickle
from PyQt4 import QtGui, QtCore

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

    def addCurve(self, min, max, avg, name = None):
        self.curves[name] = Curve(min, max, avg, self.ax)
        return

    def addLegend(self):
        lines = []
        labels = []
        for label in self.curves.keys():
            lines.append(self.curves[label].avg)
            labels.append(label)
        self.legend = self.fig.legend(lines, labels, 'upper left')
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
        x_values = range(10)#min[:,0]
        bounds = plt.fill_between(x_values, min, max, axes = ax)
        return bounds

    def getAvg(self, avg, ax, label):
        x_values = range(10)#min[:,0]
        avgPlot, = plt.plot(x_values, avg, axes = ax)
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
        x_values = range(10)
        self.bounds = plt.fill_between(x_values, min, max, axes = ax, alpha = self._alpha, color = self._color)
        return

    def setLabel(self, label):
        self.avg.set_label(label)
        return

if __name__ == '__main__':
    import numpy as np

    min = np.linspace(0,10,10)
    avg = np.linspace(0,10,10) + 3
    max = np.linspace(0,10,10) + 5

    x = carBuyingPlot()
    x.addCurve(min, max, avg, name = 'testname')
    x.addLegend()
    plt.show()