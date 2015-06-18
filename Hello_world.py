#!/usr/bin/env python

# embedding_in_qt4.py --- Simple Qt4 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

from __future__ import unicode_literals
import sys
import os
import random
import numpy as np
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtGui.QWidget(self)

        self.layout = QtGui.QGridLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)

        #test = TabBarUI(parent = self)

        #test.AddNewTab('Test!')
        #test.AddNewTab('Test2!')

        test = CarMakes()

        self.layout.addWidget(test,0,1)
        self.layout.addWidget(sc, 0, 0)
        self.layout.addWidget(dc, 1, 0)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About",
        """embedding_in_qt4.py example
        Copyright 2005 Florent Rougon, 2006 Darren Dale

        This program is a simple example of a Qt4 application embedding matplotlib
        canvases.

        It may be used and modified with no restriction; raw copies as well as
        modified versions may be distributed without limitation.""")

class CarMakes(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        super(CarMakes, self).__init__(parent)

        # ----------------
        # Create Simple UI with QTreeWidget
        # ----------------
        self.verticalLayout = QtGui.QVBoxLayout()
        #self.verticalLayout.addWidget()
        self.setLayout(self.verticalLayout)

        makes = self.getData()

        # ----------------
        # Set TreeWidget Headers
        # ----------------
        HEADERS = ( "Make", "")
        self.setColumnCount( len(HEADERS) )
        self.setHeaderLabels( HEADERS )

        for make in makes:
            makeTreeItem(name = make, parent = self)

    def getData(self):
        data = getTestData()
        makes = data.keys()
        return makes

class makeTreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, name = 'car make', parent = None):
        super(makeTreeItem, self).__init__(parent)
        self.name = name
        self.setText(0, self.name)

        self.checkBox = QtGui.QCheckBox()
        self.checkBox.clicked.connect(self.testCallback)
        #self.treeWidget().setItemWidget( self, 1, self.checkBox )
        self.treeItem = parent.setItemWidget(self, 1, self.checkBox)

    def testCallback(self, checked):
        if checked == True:
            self.item = CustomTreeItem(self, self.name)
        else:
            self.removeChild(self.item)
        return

#class buttonFactory(QtGui.QWidget):
#    boxClicked = QtCore.pyqtSignal(int)
#    colorSelected = QtCore.pyqtSignal()
#    def __init__(self, name = 'Name', parent = None):
#        super(buttonFactory, self).__init__(parent)

#        self.name = name
#        self.box = QtGui.QHBoxLayout()

#        self._checkbox()
#        self.box.addWidget(self.checkbox)

#        self.box.addWidget(self.checkbox)

#    def _checkbox(self):
#        self.checkbox = QtGui.QCheckBox(self.tr("Click me"))
#        self.connect(self.checkbox, QtCore.SIGNAL('clicked()'), self._checkboxCallback)
#        self.boxClicked.connect(boxClickedCallback)
#        return 

#    def _checkboxCallback(self):
#        print 'here!'
#        clicked = self.checkbox.isChecked()
#        self.boxClicked.emit(clicked)
#        return

#@QtCore.pyqtSlot()
#def boxClickedCallback(i):
#    print 'Clicked ', i
#    return

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
# ------------------------------------------------------------------------------
# UI
# ------------------------------------------------------------------------------
class CheckBoxUI(QtGui.QTreeWidget):
 
    def __init__( self, name = None, parent=None ):
 
        ## Init:
        super(CheckBoxUI, self).__init__(parent)
 
        # ----------------
        # Create Simple UI with QTreeWidget
        # ----------------
        self.verticalLayout = QtGui.QVBoxLayout()
        self.treeWidget = QtGui.QTreeWidget()
        self.verticalLayout.addWidget(self.treeWidget)
        self.setLayout(self.verticalLayout)

        self.name = name
 
        # ----------------
        # Set TreeWidget Headers
        # ----------------
        HEADERS = ( "column 1", "column 3", "column 2" )
        self.treeWidget.setColumnCount( len(HEADERS) )
        self.treeWidget.setHeaderLabels( HEADERS )
 
        # ----------------
        # Add Custom QTreeWidgetItem
        # ----------------
        ## Add Items:
        for name in [self.name + ' rock', 'paper', 'scissors' ]:
            item = CustomTreeItem( self.treeWidget, name )
 
        ## Set Columns Width to match content:
        for column in range( self.treeWidget.columnCount() ):
            self.treeWidget.resizeColumnToContents( column )
 
# ------------------------------------------------------------------------------
# Custom QTreeWidgetItem
# ------------------------------------------------------------------------------
class CustomTreeItem(QtGui.QTreeWidgetItem):
    '''
    Custom QTreeWidgetItem with Widgets
    '''
 
    def __init__( self, parent, name ):
        '''
        parent (QTreeWidget) : Item's QTreeWidget parent.
        name   (str)         : Item's name. just an example.
        '''
 
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeItem, self ).__init__( parent )
 
        ## Column 0 - Text:
        self.setText(0, name)
 
        ## Column 1 - SpinBox:
        self.checkBox = QtGui.QCheckBox()
        self.treeWidget().setItemWidget( self, 1, self.checkBox )
 
        # Column 2 - Button:
        self.button = QtGui.QPushButton()
        self.button.setText( "button %s" %name )
        self.treeWidget().setItemWidget( self, 2, self.button )
 
        ## Signals
        self.treeWidget().connect( self.button, QtCore.SIGNAL("clicked()"), self.buttonPressed )
 
    @property
    def name(self):
        '''
        Return name ( 1st column text )
        '''
        return self.text(0)
 
    @property
    def value(self):
        '''
        Return value ( 2nd column int)
        '''
        return self.checkBox.isChecked()
 
    def buttonPressed(self):
        '''
        Triggered when Item's button pressed.
        an example of using the Item's own values.
        '''
        print "This Item name:%s value:%i" %( self.name, self.value)


def getTestData():
    data = {}
    data['Honda'] = {}
    data['Honda']['year'] = {}
    data['Honda']['year']['2011'] = {}
    data['Honda']['year']['2011']['style'] = {}
    data['Honda']['year']['2011']['style']['DX'] = np.random.rand(10,2)
    data['Honda']['year']['2011']['style']['LS'] = np.random.rand(10,2)

    data['Honda']['year']['2012'] = {}
    data['Honda']['year']['2012']['style'] = {}
    data['Honda']['year']['2012']['style']['DX'] = np.random.rand(10,2)
    data['Honda']['year']['2012']['style']['LS'] = np.random.rand(10,2)

    data['Toyota'] = {}
    data['Toyota']['year'] = {}
    data['Toyota']['year']['2011'] = {}
    data['Toyota']['year']['2011']['style'] = {}
    data['Toyota']['year']['2011']['style']['CE'] = np.random.rand(10,2)
    data['Toyota']['year']['2011']['style']['MQ'] = np.random.rand(10,2)

    data['Toyota']['year']['2012'] = {}
    data['Toyota']['year']['2012']['style'] = {}
    data['Toyota']['year']['2012']['style']['CE'] = np.random.rand(10,2)
    data['Toyota']['year']['2012']['style']['MQ'] = np.random.rand(10,2)
    return data

if __name__ == '__main__':
    qApp = QtGui.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("%s" % progname)
    aw.show()
    sys.exit(qApp.exec_())