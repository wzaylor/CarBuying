from __future__ import unicode_literals
import sys
import os
import numpy as np
from PyQt4 import QtGui, QtCore

# Custom modules/functions
import carBuyingPlot
import Buttons

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self._fileMenu()

        self.main_widget = QtGui.QWidget(self)

        self.layout = QtGui.QGridLayout(self.main_widget)

        self.testPlot = carBuyingPlot.carBuyingPlot(name = 'boobs', parent = self)

        self._initialize()

        self.layout.addWidget(self.testPlot,0,0)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def _initialize(self):
        self.makeTabs = TabBarUI(parent = self)
        self._buttons()
        return

    def _buttons(self):
        self.buttons = Buttons.ButtonWindow(outsideCallback = self.testcallback, parent = self)
        self.layout.addWidget(self.buttons, 0, 1)
        return

    def _fileMenu(self):
        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        return

    def _addCarButton(self):
        btn = QtGui.QPushButton('Add car make')
        self.carMakesDialog = CarMakes(parent = self)
        btn.clicked.connect(self._addCarMakeCallback)
        return btn

    def _addCarMakeCallback(self):
        self.carMakesDialog.exec_()
        return

    def fileQuit(self):
        self.close()
        return

    def closeEvent(self, ce):
        self.fileQuit()
        return

    @QtCore.pyqtSlot(dict, int, str)
    def testcallback(self, data, checked, name):
        if checked == True:
            self.testPlot.addCurve(data['priceMin'], data['priceMax'], data['price'], name = name)
            self.testPlot.addLegend()
            self.testPlot.draw()
        else:
            print 'name = ', name
            self.testPlot.curves[name].bounds.remove()
            self.testPlot.curves[name].avg.remove()
            del self.testPlot.curves[name]
            self.testPlot.legend.remove()
            self.testPlot.addLegend()
            self.testPlot.draw()
        return

class TabBarUI(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(TabBarUI, self).__init__(parent)

    def AddNewTab(self, tabName):
        newTab = CheckBoxUI(name = tabName)
        self.addTab(newTab, tabName)
        return

    def getTabName(self):
        name = self.tabText(0)
        return name

if __name__ == '__main__':
    qApp = QtGui.QApplication(sys.argv)

    aw = ApplicationWindow()
    #aw.setWindowTitle("%s" % progname)
    aw.show()
    sys.exit(qApp.exec_())
    #qApp.exec_()