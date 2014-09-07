import sys
import os
import base64
from PyQt4 import QtGui, QtCore, QtWebKit
from PyQt4.QtSql import *
from DigitalStampAlbum import version
import time

class PdfUtils(QtGui.QProgressDialog):
    def __init__(self):
        super(PdfUtils, self).__init__()

    def create(self,dbname,pdfname):
        self.setStyleSheet("""
            QProgressBar {
                background-color: rgb(49,49,49);
                color: white;
                font-color: white;
            }
            QProgressBar::chunk {
                 background-color: orange;
                 width: 10px;
             }
             QWidget {
                background-color: rgb(49,49,49);
                color: white;
                font-color: white;
            }
             
            """)
        self.printer = QtGui.QPrinter()
        self.printer.setPaperSize(QtCore.QSizeF(5, 8), QtGui.QPrinter.Inch)
        self.printer.setColorMode(QtGui.QPrinter.Color)
        self.printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        self.printer.setOrientation(QtGui.QPrinter.Landscape)
        self.printer.setFullPage(False)
        self.printer.setOutputFileName(pdfname)
        
        
        self.dbname = dbname
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbname)
        
        if not self.db.open():
            print(self.db.lastError().text())
            sys.exit(1)
            
        self.sql = "select count(*) from stamps"
        self.query = QSqlQuery(self.sql, self.db)
        
        if self.query.next():
            self.count = self.query.value(0)
        
        if self.count <= 0:
            return QtGui.QMessageBox.information(self, version.AppName, "The album %s has no stamps" % (self.dbname), QtGui.QMessageBox.Ok )
        self.sql = "SELECT * FROM stamps ORDER BY id"
        self.query = QSqlQuery(self.sql, self.db)
        
        self.painter = QtGui.QPainter()

        self.pb = QtGui.QProgressDialog()
        
        self.setLabelText("Please wait...")
        
        
        self.progress = 1
        self.setRange(0,self.count)
        
        self.setWindowTitle("Exporting to PDF")
        self.setCancelButton(None)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)
        
        self.show()
        
        while (self.query.next()):
            self.setValue(self.progress)
            self.progress += 1
            self.pixmap = QtGui.QPixmap()
            self.pixmap.loadFromData(base64.b64decode(self.query.value(9)))
            if self.pixmap.width() > 300:
                    self.widthValue = 300
                    self.heightValue = ( self.pixmap.height() * 300 ) / self.pixmap.width()
                    
            elif self.pixmap.height() > 300:
                self.heightValue = 300
                self.widthValue = ( self.pixmap.width() * 300 ) / self.pixmap.height()
                    
            else:
                self.heightValue = self.pixmap.height()
                self.widthValue = self.pixmap.width()
                    
                    
            self.textEdit = QtGui.QTextDocument()          
            self.html = """
                <style type="text/css">
                
                td{font-size: 15pt;}
                
                </style>
                
                <table cellpadding="1" cellspacing="1" >
                <tbody>
		<tr>
			<td>Name</td>
			<td>%s</td>
			<td rowspan="8" ><img height="%s" width="%s" src="data:image/jpeg;base64,%s" /></td>
		</tr>
		<tr>
			<td>Year</td>
			<td>%s</td>
		</tr>
		<tr>
			<td>Date</td>
			<td>%s</td>
		</tr>
		<tr>
			<td>Country</td>
			<td>%s</td>
		</tr>
		<tr>
			<td>Color</td>
			<td>%s</td>
		</tr>
		<tr>
			<td>Theme</td>
			<td>%s</td>
		</tr>
		<tr>
			<td>Condition</td>
			<td>%s</td>
		</tr>
		<tr>
			<td>Catalog#</td>
			<td>%s</td>
		</tr>
	        </tbody>
                </table>
                <br>
                <br>

            """ % (self.query.value(1),str(self.heightValue),str(self.widthValue),bytes(self.query.value(9)).decode(),str(self.query.value(2)),self.query.value(3),self.query.value(4),self.query.value(5),self.query.value(6),self.query.value(7),self.query.value(8))
            self.textEdit.setHtml(self.html)
            self.textEdit.print_(self.printer)
            
            self.painter.begin( self.printer )
            self.textEdit.drawContents(self.painter)
            
            self.printer.newPage()
        
        QtGui.QMessageBox.information(self, version.AppName,
                    "Successfully converted to PDF \n %s" % (pdfname), QtGui.QMessageBox.Ok )
        self.painter.end()
        
        
        
