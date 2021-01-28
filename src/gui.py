""" GUI Implementation for the project using Qt5 Python bindings """

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar, QSpinBox, QDoubleSpinBox, QFrame, QGridLayout, QRadioButton, QAction, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage, QFontDatabase
from PyQt5.QtMultimedia import QSound, QSoundEffect
from PyQt5 import QtCore
from PyQt5 import QtMultimedia

import sys
import visualizer
import sorting
import time

class SortingWidget(QWidget):
    """ A widget displaying a sorting algorithm and related info """
    def __init__(self, parent, sorting_algo):
        QWidget.__init__(self, parent=parent)
        self.sorting_algo = sorting_algo
        self.layout = QVBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.setContentsMargins(10,0,10,0)

        self.name_label = QLabel()
        self.name_label.setText(sorting_algo.name)
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.metadata_label = QLabel()
        self.metadata_label.setText("comparisons: 0 reads: 0 writes: 0")
        self.metadata_label.setAlignment(QtCore.Qt.AlignCenter)

        # Sorting bitmap
        self.image_label = QLabel(self)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.metadata_label)
        self.layout.addWidget(self.image_label)

        # Setup correct fonts
        medium_font = QFont("Inter", 12)
        small_font = QFont("Inter", 10)
        self.name_label.setFont(medium_font)
        self.metadata_label.setFont(small_font)


    def render_image(self):
        """ Generate an image of a sorting list """
        if self.sorting_algo.requires_rendering(): # No point in rendering if not needed
            # Render image
            size = 800
            q_image = visualizer.list_to_bar_image(self.sorting_algo.lst, self.sorting_algo.get_coloring(), padding=3, size=size)
            pixmap = QPixmap.fromImage(q_image)
            pixmap = pixmap.scaled(size, size)
            self.image_label.setPixmap(pixmap)
            # Update sorting metadata
            self.update_sorting_metadata()
            self.update()

    def update_sorting_metadata(self):
        new_text = f'cmps: {self.sorting_algo.get_comparisons()} \t reads: {self.sorting_algo.get_reads()} \t writes: {self.sorting_algo.get_writes()}'
        self.metadata_label.setText(new_text)



class MainWindow(QWidget):
    def __init__(self, sorting_algos):
        """ Initiate the GUI Window and create all the relevant Widgets """
        super(MainWindow, self).__init__()

        self.setWindowTitle('Sorting Algorithms Visualized')
        #self.setFixedSize(825, 590)
        self.setStyleSheet("background-color: #181818; color: white")

        # Setup custom font
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("../assets/fonts/Inter-Regular.ttf")

        # Setup sounds
        self.sound_enabled = True
        self.sounds = []
        for i in range(64):
            sound = QSoundEffect()
            sound.setSource(QtCore.QUrl.fromLocalFile(f"../assets/sounds/tone-{i}.wav"))
            sound.setVolume(0.3)
            self.sounds.append(sound)

        self.is_sound_playing = lambda: False

        # Setup sorting widgets
        self.layout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignHCenter)

        self.sorting_widgets = []

        for i, algo in enumerate(sorting_algos):
            sorting_widget = SortingWidget(self, algo)
            self.layout.addWidget(sorting_widget, i // 3, i % 3)
            self.sorting_widgets.append(sorting_widget)

        self.sorting_algos = sorting_algos

        self.render_sorting()

        sorting.start_sorting(self.sorting_algos)

        # Set up rendering loop using a QTimer
        self.frame_time_sum = 0
        self.fps_update_freq = 100
        self.frame_counter = 0
        self.last_frame = None

        self.renderSorting = QtCore.QTimer(self)
        self.renderSorting.setInterval(100) #~60 FPS

        self.renderSorting.timeout.connect(self.render_timeout)
        self.renderSorting.start()

        # Render one frame
        self.running_sorting = False
        self.first_frame = True

    def render_timeout(self):
        """ Run a step of sorting algorithms and then render them to their images """
        if self.last_frame == None:
            self.last_frame = time.time()

        # Render the lists that are being sorted
        # Only render a frame if the sorting step is complete
        if (self.running_sorting or self.first_frame) and sorting.is_sorting_step_complete(self.sorting_algos):
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
        if self.sound_enabled:
            self.play_sound(self.sorting_algos[0])
        self.first_frame = False
        for widget in self.sorting_widgets:
            widget.render_image()
            # Unlock thread to allow another step of sorting
            widget.sorting_algo.unlock()

    def keyPressEvent(self, event):
        # Play/pause key
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Space:
            self.running_sorting = not self.running_sorting

    def play_sound(self, sorting_algo):
        """ Play a sound based on the last comparison. This is done using 64 different cached sound files """
        if not self.is_sound_playing() and sorting_algo.requires_rendering() and not self.first_frame:
            value = sorting_algo.lst.getitem_no_count(sorting_algo.get_sound_index()-1)
            sound_index = round((value / sorting_algo.lst.max) * 63)
            self.sounds[sound_index].play()
            self.is_sound_playing = self.sounds[sound_index].isPlaying


class MainApplication(QApplication):
    def __init__(self, sorting_algos):
        super().__init__([])

        window = MainWindow(sorting_algos)
        window.show()

        sys.exit(self.exec_())