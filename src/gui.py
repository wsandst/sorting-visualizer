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

frame_time_sum = 0
fps_update_freq = 100
frame_counter = 0
last_frame = None

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

        sorting.start_sorting(self.sorting_algos)

        self.checkThreadTimer = QtCore.QTimer(self)
        self.checkThreadTimer.setInterval(20) #.5 seconds

        self.checkThreadTimer.timeout.connect(self.sorting_timeout)
        self.checkThreadTimer.start()

    def sorting_timeout(self):
        global last_frame
        if last_frame == None:
            last_frame = time.time()

        sorting.run_sorting_step(self.sorting_algos)
        self.render_sorting()

        global frame_time_sum
        global frame_counter
        global fps_update_freq

        done = time.time()
        frame_time_sum += done - last_frame
        last_frame = done

        frame_counter += 1
        if frame_counter % fps_update_freq == 0:
            print(f'FPS: {fps_update_freq/frame_time_sum}')
            print(f'mSPF: {1000*frame_time_sum/fps_update_freq}')
            frame_time_sum = 0
    

    def render_sorting(self):
        for algo in self.sorting_algos:
            if algo.thread.is_alive():
                self.generate_sorting_image(algo.lst, algo.get_coloring())
                algo.unlock()

    def generate_sorting_image(self, lst, colors):
        q_image = visualizer.list_to_bar_image(lst, colors, padding=0)
        pixmap = QPixmap.fromImage(q_image)
        #pixmap = pixmap.scaled(400, 400)
        self.image_label.setPixmap(pixmap)


class MainApplication(QApplication):
    def __init__(self, sorting_algos):
        super().__init__([])

        window = MainWindow(sorting_algos)
        window.show()

        sys.exit(self.exec_())