""" GUI Implementation for the project using Qt5 Python bindings """

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar, QSpinBox, QDoubleSpinBox, QFrame, QGridLayout, QRadioButton
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage
from PyQt5 import QtCore

import sys

class MainWindow(QWidget):
    def __init__(self):
        """ Initiate the GUI Window and create all the relevant Widgets """
        super(MainWindow, self).__init__()

class MainApplication(QApplication):
    def __init__(self):
        super().__init__([])

        window = MainWindow()
        window.show()

        sys.exit(self.exec_())