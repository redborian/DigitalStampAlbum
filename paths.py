import os
from PyQt4 import QtGui, QtCore

#PATH for the data
MAIN_PATH = os.path.abspath(os.path.dirname(__file__))

#PATH for the DB files
DB_PATH = os.path.join(os.path.abspath(QtCore.QDir.homePath()),"Documents","Digital Stamp Album")
