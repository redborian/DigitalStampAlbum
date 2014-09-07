import sys
import os
import base64
from os.path import basename
from PyQt4 import QtGui, QtCore
from PyQt4.QtSql import *
from DigitalStampAlbum import paths
from DigitalStampAlbum.utils import getIconPath, createUserDirectory
from DigitalStampAlbum import version

class SplitWindow(QtGui.QSplitter):
    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(SplitWindow, self).__init__(orientation, parent)        

class LeftWidget(QtGui.QTreeWidget):
    def __init__(self, reference, parent=None):
        super(LeftWidget, self).__init__(parent)
        self.reference = reference
        self.setColumnCount(1)
        self.setHeaderLabels(["Album"])
        self.currentItemChanged.connect(self.handleItemChange)

    def handleItemChange(self, current, previous):
        if current.type() != -1:
            self.reference.queryCurrentSelection(current.type())

class FormLayouts(QtGui.QFormLayout):
    def __init__(self, parent=None):
        super(FormLayouts, self).__init__()
        
        
        self.nameValue = QtGui.QLineEdit()
        self.nameValue.setMaxLength(80)        
        self.addRow(QtGui.QLabel("Name"), self.nameValue)

        self.yearValue = QtGui.QLineEdit()
        self.yearValue.setMaxLength(4)
        self.yearValue.setFixedWidth(50)
        self.addRow(QtGui.QLabel("Year"), self.yearValue)

        self.dateValue = QtGui.QLineEdit()
        self.dateValue.setMaxLength(20)
        self.addRow(QtGui.QLabel("Issued Date"), self.dateValue)

        self.countryValue = QtGui.QLineEdit()
        self.countryValue.setMaxLength(20)
        self.addRow(QtGui.QLabel("Country"), self.countryValue)

        self.colorValue = QtGui.QLineEdit()
        self.colorValue.setMaxLength(20)
        self.addRow(QtGui.QLabel("Color"), self.colorValue)

        self.themeValue = QtGui.QLineEdit()
        self.themeValue.setMaxLength(20)
        self.addRow(QtGui.QLabel("Theme"), self.themeValue)

        self.conditionValue = QtGui.QLineEdit()
        self.conditionValue.setMaxLength(20)
        self.addRow(QtGui.QLabel("Condition"), self.conditionValue)

        self.catalogValue = QtGui.QLineEdit()
        self.catalogValue.setMaxLength(20)
        self.addRow(QtGui.QLabel("Catalog#"), self.catalogValue)


class RightWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        super(RightWidget, self).__init__(parent)
        
        self.hbox = QtGui.QHBoxLayout()
        self.setLayout(self.hbox)    
        
        

    def populateCurrentSelection(self):
        for cnt in reversed(range(self.hbox.count())):
            widget = self.hbox.takeAt(cnt).widget()

            if widget is not None: 
                widget.deleteLater()
        
                
        self.detailsBox = QtGui.QGroupBox("Stamp Details")      
    
        self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.sizePolicy.setHorizontalStretch(3)
        self.detailsBox.setSizePolicy(self.sizePolicy)
        self.sizePolicy.setHorizontalStretch(2)        
        
        self.formLayout = FormLayouts()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeft)
        self.formLayout.nameValue.setReadOnly(True)
        self.formLayout.yearValue.setReadOnly(True)
        self.formLayout.dateValue.setReadOnly(True)
        self.formLayout.countryValue.setReadOnly(True)
        self.formLayout.colorValue.setReadOnly(True)
        self.formLayout.themeValue.setReadOnly(True)
        self.formLayout.conditionValue.setReadOnly(True)
        self.formLayout.catalogValue.setReadOnly(True)
        
        self.imageData = QtGui.QLabel()
        self.imageData.setMaximumSize(300,300)
        
        self.detailsBox.setLayout(self.formLayout)     
        
        self.hbox.addWidget(self.detailsBox)
        self.hbox.addWidget(self.imageData)
        
        self.setLayout(self.hbox)      

    def populateFormFields(self,query):
        self.query = query
        while (self.query.next()):
            self.formLayout.nameValue.setText(self.query.value(1))
            self.formLayout.yearValue.setText(str(self.query.value(2)))
            self.formLayout.dateValue.setText(self.query.value(3))
            self.formLayout.countryValue.setText(self.query.value(4))
            self.formLayout.colorValue.setText(self.query.value(5))
            self.formLayout.themeValue.setText(self.query.value(6))
            self.formLayout.conditionValue.setText(self.query.value(7))
            self.formLayout.catalogValue.setText(self.query.value(8))
            self.byteData = self.query.value(9)
            if self.byteData:                
                self.pixmap = QtGui.QPixmap()
                self.pixmap.loadFromData(base64.b64decode(self.byteData))
                self.imageData.setPixmap(self.pixmap)
                self.imageData.setScaledContents(True)
                if self.pixmap.width() > self.imageData.maximumWidth():
                    self.imageData.setFixedWidth(300)
                    self.heightValue = ( self.pixmap.height() * 300 ) / self.pixmap.width()
                    self.imageData.setFixedHeight(self.heightValue)
                elif self.pixmap.height() > self.imageData.maximumHeight():
                    self.imageData.setFixedHeight(300)
                    self.widthValue = ( self.pixmap.width() * 300 ) / self.pixmap.height()
                    self.imageData.setFixedWidth(self.widthValue)
                else:
                    self.imageData.setFixedWidth(self.pixmap.width())
                    self.imageData.setFixedHeight(self.pixmap.height())
                
               
                    


class InputDialog(QtGui.QDialog):
   
    def __init__(self, filename,operation,stampid=None):
        super(InputDialog, self).__init__()
        
        self.mainLayout = QtGui.QVBoxLayout()
        
        self.formLayout = FormLayouts()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeft)

        if operation == 'AddStamp':
            title = "Add new stamp"
            self.imageValue = QtGui.QLineEdit()
            self.imageValue.setReadOnly(True)
            self.formLayout.addRow(QtGui.QLabel("Image Path"), self.imageValue)

            self.chooseImage = QtGui.QPushButton("Choose Image")
            self.imageButton = QtGui.QDialogButtonBox()
            self.imageButton.addButton(self.chooseImage, QtGui.QDialogButtonBox.ActionRole)
            self.formLayout.setWidget(10,QtGui.QFormLayout.FieldRole, self.imageButton)
            self.imageButton.clicked.connect(self.openImage)
        else:
            title = "Edit stamp"
            self.filename = filename
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.filename)
            self.stampid = stampid
            if not self.db.open():
                print(self.db.lastError().text())
                sys.exit(1)
            self.sql = "SELECT * FROM stamps WHERE id = " + str(self.stampid)
            self.query = QSqlQuery(self.sql, self.db)
            self.populateFormFields(self.query)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
            
            
        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.buttonBox)
        self.setWindowTitle(title)
        self.setLayout(self.mainLayout)
        self.setFixedSize(300,300)
        self.setStyleSheet("background-color: rgb(49,49,49);color: white;font-color: white;")
        
    def openImage(self):
        self.imageFile = QtGui.QFileDialog.getOpenFileName(self, 'Choose Image', QtCore.QDir.homePath(), self.tr("Image Files (*.png *.jpeg *.jpg)"))
        if self.imageFile:
            self.imageValue.setText(self.imageFile)

    def populateFormFields(self,query):
        self.query = query
        while (self.query.next()):
            self.formLayout.nameValue.setText(self.query.value(1))
            self.formLayout.yearValue.setText(str(self.query.value(2)))
            self.formLayout.dateValue.setText(self.query.value(3))
            self.formLayout.countryValue.setText(self.query.value(4))
            self.formLayout.colorValue.setText(self.query.value(5))
            self.formLayout.themeValue.setText(self.query.value(6))
            self.formLayout.conditionValue.setText(self.query.value(7))
            self.formLayout.catalogValue.setText(self.query.value(8))
        
class CentralWidget(SplitWindow):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent=parent)
        self.mainSplitter = SplitWindow(QtCore.Qt.Horizontal,self)
        
        for cnt in reversed(range(self.mainSplitter.count())):
            widget = self.mainSplitter.indexOf(cnt).widget()

            if widget is not None: 
                widget.deleteLater()
        
        self.stampsList = LeftWidget(self,self)        
        self.currentSelection = RightWidget(self)        
        self.mainSplitter.addWidget(self.stampsList)
        self.mainSplitter.addWidget(self.currentSelection)
        self.mainSplitter.setSizes([20, 180])

    def createAlbum(self,filename):
        self.filename = filename
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.filename)
        if not self.db.open():
            print(self.db.lastError().text())
            sys.exit(1)
        
        sql = "CREATE TABLE stamps (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, year NUMBER, date TEXT, country TEXT, color TEXT, theme TEXT, condition TEXT, catalogue TEXT, image BLOB)"
        QSqlQuery(sql, self.db)
        
        
            
    def openAlbum(self, filename, view='name'):
        
        self.filename = filename
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.filename)
        
        if not self.db.open():
            print(self.db.lastError().text())
            sys.exit(1)
        self.sql = "SELECT * FROM stamps ORDER BY " + view
        self.query = QSqlQuery(self.sql, self.db)

               
        while (self.query.next()):
            if view == 'name':
                self.viewBy = self.query.value(1)[0]
            elif view == 'year':
                self.viewBy = str(self.query.value(2))
            elif view == 'country':
                self.viewBy = self.query.value(4)
            else:
                self.viewBy = self.query.value(7)
            
            existingItems = self.stampsList.findItems(self.viewBy, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
            if len(existingItems) > 0:
                self.item = existingItems[0]
            else:
                self.item = QtGui.QTreeWidgetItem(self.stampsList,-1)
                self.item.setText(0, self.viewBy)
            
            self.item1 = QtGui.QTreeWidgetItem(self.item,self.query.value(0))
            self.item1.setText(0, self.query.value(1))
            
        self.stampsList.setHeaderLabels([basename(self.filename)])
        

    def addStamp(self,filename,operation,stampid=None):
        self.addDialog = InputDialog(filename, operation,stampid)
        if self.addDialog.exec_():
            if (not self.addDialog.formLayout.nameValue.displayText()) or (not self.addDialog.formLayout.yearValue.displayText()) or (not self.addDialog.formLayout.countryValue.displayText()) or (not self.addDialog.formLayout.conditionValue.displayText()):
                QtGui.QMessageBox.information(self, version.AppName,"Stamp name,country, year and condition are mandatory", QtGui.QMessageBox.Ok )
                return
            if not self.addDialog.formLayout.yearValue.displayText().isdigit():
                QtGui.QMessageBox.information(self, version.AppName,"Year value %s is not a number" % str(self.addDialog.formLayout.yearValue.displayText()), QtGui.QMessageBox.Ok )
                return
            self.filename = filename 
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.filename)
        
            if not self.db.open():
                print(self.db.lastError().text())
                sys.exit(1)
                
            if operation == 'AddStamp':
                if self.addDialog.imageValue.displayText():
                    self.fileObj = QtCore.QFile(self.addDialog.imageValue.displayText())
                    if self.fileObj.open(QtCore.QIODevice.ReadOnly):
                        self.byteArray = QtCore.QByteArray()
                        self.byteArray = self.fileObj.readAll()            
            
                self.insertSql = QSqlQuery()
                self.insertSql.prepare("INSERT INTO stamps (name,year,date,country,color,theme,condition,catalogue, image) VALUES(?,?,?,?,?,?,?,?,?)")
                self.insertSql.addBindValue(self.addDialog.formLayout.nameValue.displayText().upper())
                self.insertSql.addBindValue(self.addDialog.formLayout.yearValue.displayText())
                self.insertSql.addBindValue(self.addDialog.formLayout.dateValue.displayText().upper())
                self.insertSql.addBindValue(self.addDialog.formLayout.countryValue.displayText().upper())
                self.insertSql.addBindValue(self.addDialog.formLayout.colorValue.displayText().upper())
                self.insertSql.addBindValue(self.addDialog.formLayout.themeValue.displayText().upper())
                self.insertSql.addBindValue(self.addDialog.formLayout.conditionValue.displayText().upper())
                self.insertSql.addBindValue(self.addDialog.formLayout.catalogValue.displayText().upper())
                if self.addDialog.imageValue.displayText():
                    self.insertSql.addBindValue(self.byteArray.toBase64())
                else:
                    self.insertSql.addBindValue(self.addDialog.imageValue.displayText())
                self.insertSql.exec_()
            else:
                self.updateSql = QSqlQuery()
                self.updateSql.prepare("UPDATE stamps SET name= ? ,year = ? ,date = ? ,country = ?, color = ?,theme = ?, condition = ?, catalogue = ? WHERE id = ?")
                self.updateSql.addBindValue(self.addDialog.formLayout.nameValue.displayText().upper())
                self.updateSql.addBindValue(self.addDialog.formLayout.yearValue.displayText())
                self.updateSql.addBindValue(self.addDialog.formLayout.dateValue.displayText().upper())
                self.updateSql.addBindValue(self.addDialog.formLayout.countryValue.displayText().upper())
                self.updateSql.addBindValue(self.addDialog.formLayout.colorValue.displayText().upper())
                self.updateSql.addBindValue(self.addDialog.formLayout.themeValue.displayText().upper())
                self.updateSql.addBindValue(self.addDialog.formLayout.conditionValue.displayText().upper())
                self.updateSql.addBindValue(self.addDialog.formLayout.catalogValue.displayText().upper())
                self.updateSql.addBindValue(stampid)
                self.updateSql.exec_()

    def deleteStamp(self,stampid):
        self.stampid = stampid
        if not self.db.open():
            print(self.db.lastError().text())
            sys.exit(1)
        self.sql = "DELETE FROM stamps WHERE id = " + str(self.stampid)
        self.query = QSqlQuery(self.sql, self.db)
        
    def editImage(self,stampid,operation,newImage=None):
        if not self.db.open():
            print(self.db.lastError().text())
            sys.exit(1)
        updateSql = QSqlQuery()
        if operation == 'update':            
            updateSql.prepare("UPDATE stamps SET image = ? where id = ?")
            self.fileObj = QtCore.QFile(newImage)
            if self.fileObj.open(QtCore.QIODevice.ReadOnly):
                self.byteArray = QtCore.QByteArray()
                self.byteArray = self.fileObj.readAll()
            updateSql.addBindValue(self.byteArray.toBase64())
            updateSql.addBindValue(stampid)
            updateSql.exec_()
            QtGui.QMessageBox.information(self, version.AppName,
                    "Successfully updated image", QtGui.QMessageBox.Ok )
        else:
            updateSql.prepare("UPDATE stamps SET image = NULL where id = ?")
            updateSql.addBindValue(stampid)
            updateSql.exec_()
            QtGui.QMessageBox.information(self, version.AppName,
                    "Successfully deleted image", QtGui.QMessageBox.Ok )
        
    def queryCurrentSelection(self,stampid):
        self.stampid = stampid
        if not self.db.open():
            print(self.db.lastError().text())
            sys.exit(1)
        self.sql = "SELECT * FROM stamps WHERE id = " + str(self.stampid)
        self.query = QSqlQuery(self.sql, self.db)
        self.currentSelection.populateCurrentSelection()
        self.currentSelection.populateFormFields(self.query)



        
