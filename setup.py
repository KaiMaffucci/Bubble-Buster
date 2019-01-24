import os
import setuptools
import cx_Freeze
from cx_Freeze import *

build_exe_options = {"packages":['time','random','math','tkinter']}

os.environ['TCL_LIBRARY'] = "C:\\Users\\Kai\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\Kai\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

setup(
    name = 'BubbleBusterAlpha',
    version = "0.1",
    description = "A fun and simple bubble popping game.",
    options = {"build_exe": build_exe_options},
    executables = [Executable('BubbleBusterCode.py')],
)
