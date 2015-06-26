import sys
import numpy as np

from PyQt4 import QtGui, QtCore

# Custom modules/functions
import CarBuyingBackend as backend

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtGui.QWidget(self)

        self.layout = QtGui.QGridLayout(self.main_widget)

        self.testClass = testClass()

        self.tabBar = TabBarUI(parent = self)

        self.addTabsDialog = addTabsDialogUI(parent = self)
        self._populateTabSelectionTree()

        self.addTabBtn = addTabBtn(parent = self)
        self.addTabBtn._connectBtnSignal(self.openAddTabsDialog)

        self.layout.addWidget(self.tabBar,1,0)
        self.layout.addWidget(self.addTabBtn,0,0)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def _populateTabSelectionTree(self):
        data = backend.getCarMakes()
        for heading in data:
            CustomTreeItem(heading, callbackSlot = self.addRemoveTab, parent = self.addTabsDialog.treeWidget)
        return

    def _populateTabTree(self, tabName):
        tabIndex = self.tabBar.findTabIndex(tabName)
        if tabIndex != None:
            tabItem = self.tabBar.findTabItem(tabIndex)
            tabItem.data = backend.getMakeData(tabName)
            self.fillWidget(tabItem, tabItem.data.data)
            #x = tabItem.data
            #for model in tabItem.data.data.keys():
            #    CustomTreeItem(model, callbackSlot = self.testCallback, parent = tabItem)
        return
        
    # Callback function which is used to add tabs to the tab bar
    @QtCore.pyqtSlot(str, int)
    def addRemoveTab(self, tabName, isChecked):
        if isChecked == True:
            self.tabBar.AddNewTab(tabName)
            self._populateTabTree(tabName)
        else:
            tabIndex = self.tabBar.findTabIndex(tabName)
            if tabIndex != None:
                self.tabBar.removeTab(tabIndex)
        return

    @QtCore.pyqtSlot(str, int)
    def testCallback(self, i, checked):
        print i, checked
        return

    # Callback which is used to open the add tabs dialog box
    @QtCore.pyqtSlot()
    def openAddTabsDialog(self):
        self.addTabsDialog.show()
        return

    def fillItem(self, item, value):
        item.setExpanded(False)
        if type(value) is dict:# and 'price' not in value.keys():
            for key, val in sorted(value.iteritems()):
                if type(val) is dict:
                    if 'price' in val.keys():
                        child = CustomTreeItem(key, parent = item)
                        item.addChild(child)
                    else:
                        child = QtGui.QTreeWidgetItem()
                        child.setText(0, unicode(key))
                        item.addChild(child)
                        self.fillItem(child, val)
        elif type(value) is list:
            for val in value:
                child = QtGui.QTreeWidgetItem()
                item.addChild(child)
                if type(val) is dict:      
                    child.setText(0, '[dict]')
                    self.fillItem(child, val)
                elif type(val) is list:
                    child.setText(0, '[list]')
                    self.fillItem(child, val)
            else:
                child.setText(0, unicode(val))              
                child.setExpanded(True)
        #elif 'price' in value.keys():
        #    child = CustomTreeItem("testName!", parent = item)
        #    item.addChild(child)

    def fillWidget(self, widget, value):
        widget.clear()
        self.fillItem(widget.invisibleRootItem(), value)

class TabBarUI(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(TabBarUI, self).__init__(parent)

    def AddNewTab(self, tabName, callbackSlot = None):
        self.newTree = CheckBoxUI(name = tabName)
        self.addTab(self.newTree, tabName)
        self.data = None
        return

    def findTabIndex(self, tabName):
        stop = False
        index = 0
        while stop == False:
            name = self.tabText(index)
            if tabName == name:
                stop = True
                return index
            if index > 50: 
                stop = True
                index = None
            index += 1
        return index

    def findTabItem(self, tabIndex):
        tabItem = self.widget(tabIndex)
        return tabItem

class addTabBtn(QtGui.QPushButton):
    BtnSignal = QtCore.pyqtSignal()
    def __init__(self, text = 'text', parent = None):
        super(addTabBtn, self).__init__(parent)
        self.setText(text)

    def _connectBtnSignal(self, emitCallback):
        self.emitCallback = emitCallback
        self.connect(self, QtCore.SIGNAL('clicked()'), self.test)
        return

    def test(self):
        self.BtnSignal.connect(self.emitCallback)
        self.BtnSignal.emit()
        self.BtnSignal.disconnect()
        return

    def _disconnectBtnSignal(self):
        self.disconnect(self, QtCore.SIGNAL('clicked()'), self.emitCallback)
        return

class addTabsDialogUI(QtGui.QDialog):
    def __init__(self, parent = None):
        super(addTabsDialogUI, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.treeWidget = CheckBoxUI(parent = self)
        self.layout.addWidget(self.treeWidget)

class CheckBoxUI(QtGui.QTreeWidget):
    TreeItemSignal = QtCore.pyqtSignal(str, int)
    TreeUncheckSignal = QtCore.pyqtSignal()

    def __init__( self, name = None, callbackSlot = None, parent=None ):
 
        ## Init:
        super(CheckBoxUI, self).__init__(parent)
 
        # ----------------
        # Create Simple UI with QTreeWidget
        # ----------------
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.addWidget(self)#.treeWidget)

        self.name = name
 
class CustomTreeItem(QtGui.QTreeWidgetItem):
    '''
    Custom QTreeWidgetItem with Widgets
    '''
    def __init__(self, name, callbackSlot = None, parent = None):
        '''
        parent (QTreeWidget) : Item's QTreeWidget parent.
        name   (str)         : Item's name. just an example.
        '''
 
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(CustomTreeItem, self).__init__(parent)

        self.treeWidget().setColumnCount(2)

        self.name = name

        ## Column 0 - Text:
        self.setText(0, self.name)
 
        ## Column 1 - SpinBox:
        self.checkBox = QtGui.QCheckBox()
        self.treeWidget().setItemWidget(self, 1, self.checkBox)

        if callbackSlot != None:
            self._connectSignal(callbackSlot)

        for column in range(self.treeWidget().columnCount()):
            self.treeWidget().resizeColumnToContents(column)

    def _connectSignal(self, emitCallback):
        self.emitCallback = emitCallback
        self.checkBox.connect(self.checkBox, QtCore.SIGNAL('clicked()'), self._genericCallback)
        return

    def _disconnectSignal(self):
        self.checkBox.disconnect(self, QtCore.SIGNAL('clicked()'), self.emitCallback)
        return

    def _genericCallback(self):
        checked = self.checkBox.isChecked()
        self.treeWidget().TreeItemSignal.connect(self.emitCallback)
        self.treeWidget().TreeItemSignal.emit(self.name, checked)
        self.treeWidget().TreeItemSignal.disconnect()
        return

class testClass(object):
    value = 5
    def callback(self):
        print 'testClass callback'
        return

if __name__ == '__main__':
    qApp = QtGui.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.show()
    sys.exit(qApp.exec_())