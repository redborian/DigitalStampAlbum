import os
from PyQt4 import QtCore, QtGui
from DigitalStampAlbum import paths


def createUserDirectory():
        if not QtCore.QDir(paths.DB_PATH).exists():
                QtCore.QDir().mkdir(paths.DB_PATH)
        
def getIconPath(iconName=None):
        iconPath = os.path.join("icons",iconName)
        return QtGui.QIcon(iconPath)
