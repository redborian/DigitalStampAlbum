import sys
import os
from functools import partial
from PyQt4 import QtGui, QtCore
from PyQt4.QtSql import *
from DigitalStampAlbum import paths
from DigitalStampAlbum.CentralWidget import CentralWidget
from DigitalStampAlbum.utils import getIconPath, createUserDirectory
from DigitalStampAlbum import version
from DigitalStampAlbum.PdfUtils import PdfUtils

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        createUserDirectory()
        self.initUI()
        
    def initUI(self):
        self.viewBy = 'name'
        self.addMenusandTools()
        
        #self.centralwidget = CentralWidget(self)
        #self.setCentralWidget(self.centralwidget)
        self.statusBar()
        self.setDisplays()
        
               
        

    def addMenusandTools(self):
        self.menubar = self.menuBar()
        
        #actions for file menu        
        self.addAlbum = QtGui.QAction(getIconPath('new.png'),'&Create New Album', self)        
        self.addAlbum.setShortcut(QtGui.QKeySequence.New)
        self.addAlbum.setStatusTip('Add new album')
        self.addAlbum.triggered.connect(self.newAlbumAction)

        self.openExistingAlbum = QtGui.QAction(getIconPath('open.png'),'&Open Existing', self)        
        self.openExistingAlbum.setShortcut(QtGui.QKeySequence.Open)
        self.openExistingAlbum.setStatusTip('Open existing album')
        self.openExistingAlbum.triggered.connect(self.openAlbumAction)
 
        self.exitAction = QtGui.QAction(getIconPath('exit.png'),'&Exit', self)        
        self.exitAction.setShortcut(QtGui.QKeySequence.Quit)
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

        #creating filemenu and adding actions
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.addAlbum)
        self.fileMenu.addAction(self.openExistingAlbum)
        self.fileMenu.addAction(self.exitAction)

        #actions for album menu

        self.addStamp = QtGui.QAction(getIconPath('addStamps.png'),'&Add Stamp', self)
        self.addStamp.setShortcut(QtGui.QKeySequence.ZoomIn)
        self.addStamp.setStatusTip('Add new stamp to the current album')
        self.addStamp.setDisabled(True)
        self.addStamp.triggered.connect(self.addStampAction)

        self.exportPdf = QtGui.QAction(getIconPath('exportPdf.png'),'&Export as PDF', self)
        self.exportPdf.setShortcut(QtGui.QKeySequence.Print)
        self.exportPdf.setStatusTip('Save the current album as PDF')
        self.exportPdf.setDisabled(True)
        self.exportPdf.triggered.connect(self.exportToPdf)
		
        self.albumMenu = self.menubar.addMenu('&Album')
        self.albumMenu.addAction(self.addStamp)
        self.albumMenu.addAction(self.exportPdf)

        #actions for Stamp Menu

        self.editStamp = QtGui.QAction(getIconPath('editStamps.png'),'&Edit Stamp', self)
        self.editStamp.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.editStamp.setStatusTip('Edit details for the current selection')
        self.editStamp.setDisabled(True)
        self.editStamp.triggered.connect(self.editStampAction)

        self.editImage = QtGui.QAction(getIconPath('editImage.png'),'&Add/Edit Image', self)
        self.editImage.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.editImage.setStatusTip('Add/Edit image for the current selection')
        self.editImage.setDisabled(True)
        self.editImage.triggered.connect(self.editImageAction)
	
        self.deleteStamp = QtGui.QAction(getIconPath('deleteStamps.png'),'&Delete Stamp', self)
        self.deleteStamp.setShortcut(QtGui.QKeySequence.ZoomOut)
        self.deleteStamp.setStatusTip('Delete the current selection')
        self.deleteStamp.setDisabled(True)
        self.deleteStamp.triggered.connect(self.deleteStampAction)

        self.stampMenu = self.menubar.addMenu('&Stamp')
        self.stampMenu.addAction(self.editStamp)
        self.stampMenu.addAction(self.editImage)
        self.stampMenu.addAction(self.deleteStamp)
                
        #actions for View Menu

        self.nameView = QtGui.QAction(getIconPath('viewBy.png'),'&By Name', self)
        #self.nameView.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.nameView.setStatusTip('Group stamps by name')
        self.nameView.setDisabled(True)
        self.nameView.triggered.connect(partial(self.setView,'name'))

        self.yearView = QtGui.QAction(getIconPath('viewBy.png'),'&By Year', self)
        #self.yearView.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.yearView.setStatusTip('Group stamps by year')
        self.yearView.setDisabled(True)
        self.yearView.triggered.connect(partial(self.setView,'year'))

        self.countryView = QtGui.QAction(getIconPath('viewBy.png'),'&By Country', self)
        #self.countryView.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.countryView.setStatusTip('Group stamps by country')
        self.countryView.setDisabled(True)
        self.countryView.triggered.connect(partial(self.setView,'country'))

        self.conditionView = QtGui.QAction(getIconPath('viewBy.png'),'&By Condition', self)
        #self.conditionView.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.conditionView.setStatusTip('Group stamps by condition')
        self.conditionView.setDisabled(True)
        self.conditionView.triggered.connect(partial(self.setView,'condition'))

        self.viewMenu = self.menubar.addMenu('&View')
        self.viewMenu.addAction(self.nameView)
        self.viewMenu.addAction(self.yearView)
        self.viewMenu.addAction(self.countryView)
        self.viewMenu.addAction(self.conditionView)
                
        #----------------------------------------------------------------------------------------------------------------
        #define toolbar and add actions
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.addAlbum)
        self.toolbar.addAction(self.openExistingAlbum)
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.addStamp)
        self.toolbar.addAction(self.exportPdf)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.editStamp)
        self.toolbar.addAction(self.editImage)
        self.toolbar.addAction(self.deleteStamp)
        
        
    
    
    def setDisplays(self):
        self.setWindowTitle(version.AppName)
        self.setWindowIcon(getIconPath('titleIcon.png'))
        self.setFixedSize(800, 500)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        self.setStyleSheet("""
           QMenuBar {
               background-color: rgb(49,49,49);
               color: rgb(255,255,255);
               
           }
 
           QMenuBar::item {
               background-color: rgb(49,49,49);
               color: rgb(255,255,255);
           }
 
           QMenuBar::item::selected {
               background-color: orange;
               color: white;
           }
 
           QMenu {
               background-color: rgb(49,49,49);
               color: rgb(255,255,255);
           }
           QMenu::item {
               background-color: rgb(49,49,49);
               color: white;
           }
 
           QMenu::item::selected {
               background-color: orange;
               color: white;
               
           }
           QToolBar {
               background-color: rgb(49,49,49);
               color: rgb(255,255,255);              
           }
           QToolBar::separator {
               background-color: rgb(49,49,49);
               color: orange;              
           }
           QWidget {
               background-color: rgb(49,49,49);
               color: white;
               font-color: white;
           }
           QDialog {
               background-color: rgb(49,49,49);
               color: white;
               font-color: white;
           }
           QProgressBar::chunk {
                 background-color: orange;               
                 
             }
           QFormLayout {
               background-color: rgb(49,49,49);
               color: white;
               font-color: white;
           }
           QTreeWidget {
               background-color: rgb(49,49,49);
               color: white;
               font-color: white;
           }
           QTreeWidget::item::selected {
               background-color: rgb(49,49,49);
               color: orange;
               font-color: white;
           }
           QTreeView::branch:open:has-children{
               image: url(icons/branchOpen.png);
            }
            QTreeView::branch:closed:has-children {
               image: url(icons/branchClosed.png);
            }
            QHeaderView::section {
                background-color: rgb(49,49,49);
               color: white;
            }
                     
       """)

        self.show()
    
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, version.AppName,
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        
        
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            self.populateCentralWidget()
            
    def refreshAction(self):
        self.addStamp.setEnabled(True)
        self.deleteStamp.setEnabled(True)
        self.editStamp.setEnabled(True)
        self.exportPdf.setEnabled(True)
        self.editImage.setEnabled(True)
        self.nameView.setEnabled(True)
        self.yearView.setEnabled(True)
        self.countryView.setEnabled(True)
        self.conditionView.setEnabled(True)
        
    def populateCentralWidget(self):
        self.centralwidget = CentralWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.openAlbum(self.filename,self.viewBy)
        self.refreshAction()

    def setView(self,view):
        self.viewBy = view
        self.populateCentralWidget()
    
    def newAlbumAction(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,
                self.tr("Create New Album"), paths.DB_PATH,
                self.tr("Albums (*.album)"))
        if os.path.isfile(filename):
            os.remove(filename)
        if filename:
            self.filename = filename
            self.centralwidget = CentralWidget(self)
            self.setCentralWidget(self.centralwidget)
            self.centralwidget.createAlbum(self.filename)
            self.centralwidget.openAlbum(self.filename)
            self.refreshAction()

    def openAlbumAction(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Album', paths.DB_PATH, self.tr("Albums (*.album)"))
        if filename:
            self.filename = filename
            self.populateCentralWidget()

    def addStampAction(self):
        if self.filename:
            self.centralwidget.addStamp(self.filename,"AddStamp")
            self.populateCentralWidget()

    def deleteStampAction(self):
        if not hasattr(self.centralwidget, 'stampid'):
            noStampExist = QtGui.QMessageBox.information(self, version.AppName,
            "Please select a stamp to delete", QtGui.QMessageBox.Ok )
            
        else:            
            deleteConfirm = QtGui.QMessageBox.question(self, version.AppName,
                "This action cannot be undone. Are you sure want to delete the selected stamp?", QtGui.QMessageBox.Yes | 
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                      
            if deleteConfirm == QtGui.QMessageBox.Yes:
                self.centralwidget.deleteStamp(self.centralwidget.stampid)
                self.populateCentralWidget()
            
    def editStampAction(self):
        if not hasattr(self.centralwidget, 'stampid'):
            noStampExist = QtGui.QMessageBox.information(self, version.AppName,
            "Please select a stamp to edit", QtGui.QMessageBox.Ok )
            
        else:
            self.centralwidget.addStamp(self.filename,"EditStamp",self.centralwidget.stampid)
            self.populateCentralWidget()
            
    def editImageAction(self):
        if not hasattr(self.centralwidget, 'stampid'):
            noStampExist = QtGui.QMessageBox.information(self, version.AppName,
            "Please select a stamp to edit", QtGui.QMessageBox.Ok )
        else:
            self.editImageDialog = QtGui.QDialog()
            self.editImageDialog.setWindowTitle("Add/Edit Image")
            self.editImageDialog.setGeometry(300, 300, 290, 150)
            mainLayout = QtGui.QHBoxLayout()
            addImageButton = QtGui.QPushButton("Choose new image")
            deleteImageButton = QtGui.QPushButton("Delete current image")
            
            self.editImageDialog.setLayout(mainLayout)
            mainLayout.addWidget(addImageButton)
            mainLayout.addWidget(deleteImageButton)
            addImageButton.clicked.connect(partial(self.editImageActionWrapper,'update'))
            deleteImageButton.clicked.connect(partial(self.editImageActionWrapper,'delete'))
            self.editImageDialog.setStyleSheet("background-color: rgb(49,49,49);color: white;font-color: white;")
            
            self.editImageDialog.setModal(True)
            self.editImageDialog.setFixedSize(250, 50)
            self.editImageDialog.setWindowIcon(getIconPath('titleIcon.png'))
            self.editImageDialog.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            self.editImageDialog.show()
            
    def editImageActionWrapper(self,operation):
        if operation == 'update':
            newImage = QtGui.QFileDialog.getOpenFileName(self, 'Choose Image', QtCore.QDir.homePath(), self.tr("Image Files (*.png *.jpeg *.jpg)"))
            if newImage:
                self.centralwidget.editImage(self.centralwidget.stampid,operation,newImage)
        else:
            self.centralwidget.editImage(self.centralwidget.stampid,operation)
        self.editImageDialog.close()
        self.populateCentralWidget()
        
    def exportToPdf(self):
        if self.filename:
            self.pdfFile = QtGui.QFileDialog.getSaveFileName(self,
                self.tr("Create PDF"), paths.DB_PATH,
                self.tr("PDF (*.pdf)"))
            if self.pdfFile:
                self.pdfutils = PdfUtils()

                self.pdfutils.create(self.filename,self.pdfFile)
                    
                self.populateCentralWidget()
