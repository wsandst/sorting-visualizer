""" GUI Implementation for the project using Qt5 Python bindings """

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar, QSpinBox, QDoubleSpinBox, QFrame, QGridLayout, QRadioButton
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage
from PyQt5 import QtCore

import sys
import visualizer

class MainWindow(QWidget):
    def __init__(self):
        """ Initiate the GUI Window and create all the relevant Widgets """
        super(MainWindow, self).__init__()

        self.setWindowTitle('Sorting Algorithms Visualized')
        self.setFixedSize(825, 590)
        self.setStyleSheet("background-color: #181818; color: white")

        self.main_layout = QHBoxLayout()

        self.image_label = QLabel(self)
        self.main_layout.addWidget(self.image_label)

        self.update_image()

    def update_image(self):
        q_image = visualizer.list_to_bar_image([])
        pixmap = QPixmap.fromImage(q_image)
        #pixmap = pixmap.scaled(400, 400)
        self.image_label.setPixmap(pixmap)

class MainApplication(QApplication):
    def __init__(self):
        super().__init__([])

        window = MainWindow()
        window.show()

        sys.exit(self.exec_())