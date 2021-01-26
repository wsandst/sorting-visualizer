""" GUI Implementation for the project using Qt5 Python bindings """

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar, QSpinBox, QDoubleSpinBox, QFrame, QGridLayout, QRadioButton, QAction, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage
from PyQt5 import QtCore

import sys
import visualizer
import sorting
import time

class SortingWidget(QWidget):
    def __init__(self, parent, sorting_algo):
        QWidget.__init__(self, parent=parent)
        self.sorting_algo = sorting_algo
        self.layout = QVBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.setContentsMargins(0,0,0,0)

        self.name_label = QLabel()
        self.name_label.setText(sorting_algo.name)
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.metadata_label = QLabel()
        self.metadata_label.setText("comparisons: 0 reads: 0 writes: 0")
        self.metadata_label.setAlignment(QtCore.Qt.AlignCenter)

        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )

        self.image_label = QLabel(self)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.metadata_label)
        self.layout.addWidget(self.image_label)

    #def sizeHint(self):
        #return QtCore.QSize(400,400)

    def render_image(self):
        """ Generate an image of a sorting list """
        if self.sorting_algo.thread.is_alive(): # No point in rendering once the algorithm is done
            # Render image
            q_image = visualizer.list_to_bar_image(self.sorting_algo.lst, self.sorting_algo.get_coloring(), padding=2)
            pixmap = QPixmap.fromImage(q_image)
            pixmap = pixmap.scaled(400, 400)
            self.image_label.setPixmap(pixmap)
            # Update sorting metadata
            self.update_sorting_metadata()
            self.update()

    def update_sorting_metadata(self):
        new_text = f'comparisons: {self.sorting_algo.get_comparisons()} reads: {self.sorting_algo.get_reads()} writes: {self.sorting_algo.get_writes()}'
        self.metadata_label.setText(new_text)

class MainWindow(QWidget):
    def __init__(self, sorting_algos):
        """ Initiate the GUI Window and create all the relevant Widgets """
        super(MainWindow, self).__init__()

        self.setWindowTitle('Sorting Algorithms Visualized')
        #self.setFixedSize(825, 590)
        self.setStyleSheet("background-color: #181818; color: white")

        self.layout = QHBoxLayout(self)

        self.sorting_widgets = []

        for algo in sorting_algos:
            sorting_widget = SortingWidget(self, algo)
            self.layout.addWidget(sorting_widget)
            self.sorting_widgets.append(sorting_widget)


        self.sorting_algos = sorting_algos

        self.render_sorting()

        sorting.start_sorting(self.sorting_algos)

        # Set up rendering loop
        self.frame_time_sum = 0
        self.fps_update_freq = 100
        self.frame_counter = 0
        self.last_frame = None

        self.renderSorting = QtCore.QTimer(self)
        self.renderSorting.setInterval(18) #~60 FPS

        self.renderSorting.timeout.connect(self.render_timeout)
        self.renderSorting.start()

    def render_timeout(self):
        """ Run a step of sorting algorithms and then render them to their images """
        if self.last_frame == None:
            self.last_frame = time.time()

        # Run sorting algorithms one step
        sorting.run_sorting_step(self.sorting_algos)
        # Render the lists that are being sorted
        self.render_sorting()

        # Calculate FPS and print it
        end = time.time()
        self.frame_time_sum += end - self.last_frame
        self.last_frame = end

        self.frame_counter += 1
        if self.frame_counter % self.fps_update_freq == 0:
            print(f'FPS: {self.fps_update_freq/self.frame_time_sum} ({1000*self.frame_time_sum/self.fps_update_freq}ms)')
            self.frame_time_sum = 0
    

    def render_sorting(self):
        """ Render images of all the lists being sorted """
        for widget in self.sorting_widgets:
            widget.render_image()
            widget.sorting_algo.unlock()



class MainApplication(QApplication):
    def __init__(self, sorting_algos):
        super().__init__([])

        window = MainWindow(sorting_algos)
        window.show()

        sys.exit(self.exec_())