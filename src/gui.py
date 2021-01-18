""" GUI Implementation for the project using Qt5 Python bindings """

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar, QSpinBox, QDoubleSpinBox, QFrame, QGridLayout, QRadioButton
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage
from PyQt5 import QtCore

import sys
import visualizer
import sorting


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

        self.update_image(self.sorting_algos[0].lst)

        self.checkThreadTimer = QtCore.QTimer(self)
        self.checkThreadTimer.setInterval(500) #.5 seconds

        self.checkThreadTimer.timeout.connect(self.sorting_timeout)
        self.checkThreadTimer.start()

        sorting.start_sorting(self.sorting_algos)

    def update_image(self, lst):
        q_image = visualizer.list_to_bar_image(lst)
        pixmap = QPixmap.fromImage(q_image)
        #pixmap = pixmap.scaled(400, 400)
        self.image_label.setPixmap(pixmap)

    def sorting_timeout(self):
        print("Updating image")
        self.run_sorting_one_step(self.sorting_algos)

    def run_sorting_one_step(self, sorting_algos):
        any_thread_alive = False
        for algo in sorting_algos:
            if not algo.is_thread_locked():
                return False
            any_thread_alive = any_thread_alive or algo.thread.is_alive()
        if not any_thread_alive:
            return False
            
        print("Running algos")
        for algo in sorting_algos:
            if algo.thread.is_alive():
                self.update_image(algo.lst)
                algo.unlock()


class MainApplication(QApplication):
    def __init__(self, sorting_algos):
        super().__init__([])

        window = MainWindow(sorting_algos)
        window.show()

        sys.exit(self.exec_())