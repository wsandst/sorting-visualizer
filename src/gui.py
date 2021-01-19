""" GUI Implementation for the project using Qt5 Python bindings """

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar, QSpinBox, QDoubleSpinBox, QFrame, QGridLayout, QRadioButton, QAction
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage
from PyQt5 import QtCore

import sys
import visualizer
import sorting
import time


class MainWindow(QWidget):
    def __init__(self, sorting_algos):
        """ Initiate the GUI Window and create all the relevant Widgets """
        super(MainWindow, self).__init__()

        self.setWindowTitle('Sorting Algorithms Visualized')
        self.setFixedSize(825, 590)
        self.setStyleSheet("background-color: #181818; color: white")

        self.main_layout = QHBoxLayout()

        self.image_label = QLabel(self)
        self.main_layout.addWidget(self.image_label)

        self.sorting_algos = sorting_algos

        self.generate_sorting_image(self.sorting_algos[0].lst, self.sorting_algos[0].get_coloring())

        self.checkThreadTimer = QtCore.QTimer(self)
        self.checkThreadTimer.setInterval(20) #.5 seconds

        self.checkThreadTimer.timeout.connect(self.sorting_timeout)
        self.checkThreadTimer.start()

        sorting.start_sorting(self.sorting_algos)

    def sorting_timeout(self):
        start = time.time()

        sorting.run_sorting_step(self.sorting_algos)
        self.render_sorting()

        elapsed = time.time() - start
        print(f'Frame took {elapsed}s')
    

    def render_sorting(self):
        for algo in self.sorting_algos:
            if algo.thread.is_alive():
                self.generate_sorting_image(algo.lst, algo.get_coloring())
                algo.unlock()

    def generate_sorting_image(self, lst, colors):
        q_image = visualizer.list_to_bar_image(lst, colors, padding=2)
        pixmap = QPixmap.fromImage(q_image)
        #pixmap = pixmap.scaled(400, 400)
        self.image_label.setPixmap(pixmap)


class MainApplication(QApplication):
    def __init__(self, sorting_algos):
        super().__init__([])

        window = MainWindow(sorting_algos)
        window.show()

        sys.exit(self.exec_())