from __future__ import unicode_literals
import sys
import os
import numpy as np
from PyQt4 import QtGui, QtCore

# Custom modules/functions
import carBuyingPlot

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

        #self.carMakeTabs = TabBarUI(parent = self)

        self.layout.addWidget(self.testPlot,0,0)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def _initialize(self):
        self.addCarBtn = self._addCarButton()
        self.makeTabs = TabBarUI(parent = self)
        self.layout.addWidget(self.addCarBtn, 0, 1)
        self.layout.addWidget(self.makeTabs, 0, 2)
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

class CarMakes(QtGui.QDialog):
    makeSelectionSignal = QtCore.pyqtSignal(int, str)
    def __init__(self, parent = None):
        super(CarMakes, self).__init__(parent)
        self.parent = parent
        # ----------------
        # Create Simple UI with QTreeWidget
        # ----------------
        self.verticalLayout = QtGui.QVBoxLayout()
        self.setLayout(self.verticalLayout)

        self.treeWidget = QtGui.QTreeWidget(self.parent)
        self.verticalLayout.addWidget(self.treeWidget)

        self.makeNames = self.getData()

        # ----------------
        # Set TreeWidget Headers
        # ----------------
        HEADERS = ( "Make", "")
        self.treeWidget.setColumnCount( len(HEADERS) )
        self.treeWidget.setHeaderLabels( HEADERS )

        for make in self.makeNames:
            makeTreeItem(name = make, parent = self.treeWidget,
                        callback = self.makeCallback, signal = self.makeSelectionSignal)

    def getData(self):
        data = getTestData()
        makes = data.keys()
        return makes

    def makeCallback(self, checked, makeName):
        if checked == True:
            newTab = makeCheckBoxTree(str(makeName), self)
            #newTab = CheckBoxUI(name = makeName)
            self.parent.makeTabs.addTab(newTab, makeName)
        else:
            pass
        return

class makeTreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, name = 'car make', callback = None, signal = None, parent = None):
        super(makeTreeItem, self).__init__(parent)
        self.name = name
        self.setText(0, self.name)
        self.parent = parent
        self.signal = signal
        self.callback = callback

        self.checkBox = QtGui.QCheckBox()
        if callback == None:
            self.checkBox.clicked.connect(self.testCallback)
        else:
            self.checkBox.connect(self.checkBox, QtCore.SIGNAL('clicked()'), self._callback)
        #self.treeWidget().setItemWidget( self, 1, self.checkBox )
        self.parent.treeItem = parent.setItemWidget(self, 1, self.checkBox)

    def testCallback(self, checked):
        if checked == True:
            self.item = CustomTreeItem(self, self.name)
        else:
            self.removeChild(self.item)
        return

    def _callback(self):
        print 'makeTreeItem callback!'
        self.callback(self.checkBox.isChecked(), self.name)
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

def makeCheckBoxTree(makeName, parent):
    data = getTestData(makeName = makeName)
    newTab = CheckBoxUI(name = makeName, parent = parent)
    for modelName in data.keys():
        modelItem = QtGui.QTreeWidgetItem(modelName)
        modelBranch = newTab.itemBelow(modelItem)
        for year in data[modelName].keys():
            yearBranch = CustomTreeItem(modelBranch, year)
            for style in data[modelName][year].keys():
                styleBranch = CustomTreeItem(yearBranch, style)

    return newTab

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
        HEADERS = ( "Model", "", "" )
        self.treeWidget.setColumnCount( len(HEADERS) )
        self.treeWidget.setHeaderLabels( HEADERS )
 
        # ----------------
        # Add Custom QTreeWidgetItem
        # ----------------
        # Add Items:
        #item = CustomTreeItem(self.treeWidget, name)
 
        ## Set Columns Width to match content:
        for column in range( self.treeWidget.columnCount() ):
            self.treeWidget.resizeColumnToContents( column )

    def addTreeItem(self, itemName):
        return

    def addTreeItemCheckbox(self,  itemName):
        item = CustomTreeItem(self.treeWidget, itemName)
        return item
 
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

def getTestData(makeName = None):
    data = {}
    data['Honda'] = {}
    data['Honda']['Civic'] = {}
    data['Honda']['Civic']['2011'] = {}
    data['Honda']['Civic']['2011']['DX'] = np.random.rand(10,2)
    data['Honda']['Civic']['2011']['LS'] = np.random.rand(10,2)

    data['Honda']['Civic'] = {}
    data['Honda']['Civic']['2012'] = {}
    data['Honda']['Civic']['2012']['DX'] = np.random.rand(10,2)
    data['Honda']['Civic']['2012']['LS'] = np.random.rand(10,2)

    data['Toyota'] = {}
    data['Toyota']['Carolla'] = {}
    data['Toyota']['Carolla']['2011'] = {}
    data['Toyota']['Carolla']['2011']['DX'] = np.random.rand(10,2)
    data['Toyota']['Carolla']['2011']['LS'] = np.random.rand(10,2)

    data['Toyota']['Carolla'] = {}
    data['Toyota']['Carolla']['2012'] = {}
    data['Toyota']['Carolla']['2012']['EY'] = np.random.rand(10,2)
    data['Toyota']['Carolla']['2012']['MT'] = np.random.rand(10,2)

    if makeName == None:
        return data
    else:
        return data[makeName]


if __name__ == '__main__':
    qApp = QtGui.QApplication(sys.argv)

    aw = ApplicationWindow()
    #aw.setWindowTitle("%s" % progname)
    aw.show()
    sys.exit(qApp.exec_())
    #qApp.exec_()