import sys
import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt4 import QtGui, QtCore

from DigitalStampAlbum.MainWindow import MainWindow

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
