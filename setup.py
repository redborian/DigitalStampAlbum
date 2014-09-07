import sys
import os
import PyQt4
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
main_python_file = "main.py" #the name of the python file you use to run the program

from DigitalStampAlbum import version
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    executable_ext = ".exe"
    qt_dir = PyQt4.__path__[0]
print(qt_dir)
include_files = [
		("icons", "icons"),
		(qt_dir + "/plugins/imageformats", "imageformats")
]
include_files.append(
                (qt_dir + "/plugins/sqldrivers/qsqlite4.dll", "sqldrivers/qsqlite4.dll"))
includes = ["atexit","re","PyQt4.QtNetwork"]
build_exe_options = {
            "includes": includes,
            "include_files": include_files,
            "replace_paths": [(os.path.dirname(__file__) + os.sep, '')]
}
setup(
        name = version.AppName,
        version = version.Version,
        description = "A windows desktop application for Philatelists to value, organize and track their stamp collection quickly & easily. Includes features like exporting album to PDF. ",
        options = {"build_exe": build_exe_options},
        executables = [Executable(main_python_file, base = base,icon='icons/titleIcon.ico',targetName=version.AppName + executable_ext)])
