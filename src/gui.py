""" GUI Implementation for the project using Qt5 Python bindings """

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget, QCheckBox, QSpacerItem, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QGridLayout, QAction, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage, QFontDatabase
from PyQt5.QtMultimedia import QSound, QSoundEffect
from PyQt5 import QtCore
from PyQt5 import QtMultimedia

from enum import Enum
import sys
import time

import visualizer
import sorting
import special_types
from sorting import SortingAlgorithm

SortRenderType = Enum("SortingRenderingType", "BarGraph PointGraph PointSpiral PointCircle")

class SortingWidget(QWidget):
    """ A widget displaying a sorting algorithm and related info """
    def __init__(self, parent, sorting_algo):
        super(SortingWidget, self).__init__(parent)
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
        self.image_label.setMinimumSize(384, 384)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.metadata_label)
        self.layout.addWidget(self.image_label) 

        # Setup correct fonts
        medium_font = QFont("Inter", 12)
        small_font = QFont("Inter", 10)
        self.name_label.setFont(medium_font)
        self.metadata_label.setFont(small_font)


    def generateImage(self, rendering_type, rainbow):
        """ Generate an image of a sorting list """
        if self.sorting_algo.requires_rendering(): # No point in rendering if not needed
            # Render image
            size = 384
            q_image = None
            if rendering_type == SortRenderType.BarGraph:
                q_image = visualizer.list_to_bar_graph(self.sorting_algo.lst, self.sorting_algo.get_coloring(), padding=3, size=size, rainbow=rainbow)
            elif rendering_type == SortRenderType.PointGraph:
                q_image = visualizer.list_to_point_graph(self.sorting_algo.lst, self.sorting_algo.get_coloring(), padding=3, size=size, rainbow=rainbow)
            elif rendering_type == SortRenderType.PointSpiral:
                q_image = visualizer.list_to_point_spiral(self.sorting_algo.lst, self.sorting_algo.get_coloring(), padding=3, size=size, rainbow=rainbow)
            elif rendering_type == SortRenderType.PointCircle:
                q_image = visualizer.list_to_point_disparity(self.sorting_algo.lst, self.sorting_algo.get_coloring(), padding=3, size=size, rainbow=rainbow)
            pixmap = QPixmap.fromImage(q_image)
            pixmap = pixmap.scaled(size, size)
            self.image_label.setPixmap(pixmap)
            # Update sorting metadata
            self.updateSortingMetadata()
            self.update()

    def updateSortingMetadata(self):
        new_text = f'cmps: {self.sorting_algo.get_comparisons()} \t reads: {self.sorting_algo.get_reads()} \t writes: {self.sorting_algo.get_writes()}'
        self.metadata_label.setText(new_text)


class SortingTab(QWidget):
    def __init__(self, parent):
        """ Tab window for visualising Sorting Algorithms """
        super(SortingTab, self).__init__(parent)

        # Setup sounds
        self.sound_enabled = False
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

        self.rendering_type = SortRenderType.BarGraph
        self.rainbow = False

    def updateSortingAlgorithms(self, sorting_algos):
        self.sorting_widgets = []

        for i, algo in enumerate(sorting_algos):
            sorting_widget = SortingWidget(self, algo)
            self.layout.addWidget(sorting_widget, i // 4, i % 4)
            self.sorting_widgets.append(sorting_widget)

        self.sorting_algos = sorting_algos

    def startRendering(self):
        self.renderSorting()

        sorting.start_sorting(self.sorting_algos)

        # Set up rendering loop using a QTimer
        self.frame_time_sum = 0
        self.fps_update_freq = 100
        self.frame_counter = 0
        self.last_frame = None

        self.render_timer = QtCore.QTimer(self)
        self.current_frame_time = 64
        self.sorting_speed_mult = 1
        self.render_timer.setInterval(self.current_frame_time) #~60 FPS

        self.render_timer.timeout.connect(self.renderTimeout)
        self.render_timer.start()

        # Render one frame
        self.running_sorting = False
        self.first_frame = True

    def renderTimeout(self):
        """ Run a step of sorting algorithms and then render them to their images """
        if self.last_frame == None:
            self.last_frame = time.time()

        # Render the lists that are being sorted
        # Only render a frame if the sorting step is complete
        if (self.running_sorting or self.first_frame) and sorting.is_sorting_step_complete(self.sorting_algos):
            self.renderSorting()

        # Calculate FPS and print it
        end = time.time()
        self.frame_time_sum += end - self.last_frame
        self.last_frame = end

        self.frame_counter += 1
        if self.frame_counter % self.fps_update_freq == 0:
            print(f'FPS: {self.fps_update_freq/self.frame_time_sum} ({1000*self.frame_time_sum/self.fps_update_freq}ms)')
            self.frame_time_sum = 0
        

    def renderSorting(self):
        """ Render images of all the lists being sorted """
        if self.sound_enabled:
            self.playSound(self.sorting_algos[0])
        self.first_frame = False
        for widget in self.sorting_widgets:
            widget.generateImage(self.rendering_type, self.rainbow)
            # Unlock thread to allow another step of sorting
            widget.sorting_algo.unlock()

    def keyPressEvent(self, event):
        # Play/pause key
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Space:
            self.running_sorting = not self.running_sorting
        if event.key() == Qt.Key_Right:
            self.modifySpeed(0.5)
        if event.key() == Qt.Key_Left:
            self.modifySpeed(2)

    def modifySpeed(self, scale):
        """ Increases the speed of the sorting visualization """
        if self.current_frame_time <= 16 and (special_types.ThreadManagment.cmp_before_lock != 1 or scale < 1): 
            # Already at ~60 FPS, modify comparisons allowed
            special_types.ThreadManagment.cmp_before_lock = int(max(1, special_types.ThreadManagment.cmp_before_lock / scale))
        else:
            self.current_frame_time = max(16, scale*self.current_frame_time)
            special_types.ThreadManagment.cmp_before_lock = 1
            
        self.render_timer.setInterval(self.current_frame_time)
        #print(f"Speed modified to {self.current_frame_time} ms, {special_types.ThreadManagment.cmp_before_lock} cmp_before_lock")

    def playSound(self, sorting_algo):
        """ Play a sound based on the last comparison. This is done using 64 different cached sound files """
        if not self.is_sound_playing() and sorting_algo.requires_rendering() and not self.first_frame:
            value = sorting_algo.lst.getitem_no_count(sorting_algo.get_sound_index()-1)
            sound_index = round((value / sorting_algo.lst.max) * 63)
            self.sounds[sound_index].play()
            self.is_sound_playing = self.sounds[sound_index].isPlaying

class SelectionTab(QWidget):
    def __init__(self, parent, sorting_func_map, main_window):
        super(SelectionTab, self).__init__(parent)
        self.sorting_func_map = sorting_func_map

        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10,10,10,10)
        self.layout.setAlignment(Qt.AlignTop)


        self.hlayout = QHBoxLayout(self)
        self.vlayout = QVBoxLayout(self)
        self.layout.addLayout(self.hlayout)
        self.hlayout.addLayout(self.vlayout)
        self.hlayout.setSpacing(15)
        #self.hlayout.setAlignment(Qt.AlignLeft)

        self.vlayout.setAlignment(Qt.AlignTop)
        self.vlayout.setSpacing(10)

        # Select sorting algorithms
        label = QLabel()
        label.setText("Select Sorting Algorithms")
        self.vlayout.addWidget(label)
        self.sorting_selections = []
        for i in range(8):
            sorting_selection = QComboBox(self)
            sorting_selection.setMinimumWidth(150)
            sorting_selection.addItems(sorting_func_map.keys())
            self.sorting_selections.append(sorting_selection)
            self.vlayout.addWidget(sorting_selection, Qt.AlignLeft)

        # Separator
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)
        separator_line.setStyleSheet("QFrame { color : #535353; }")
        separator_line.setLineWidth(1)
        self.hlayout.addWidget(separator_line)

        # Select drawing options
        self.vlayout2 = QVBoxLayout(self)
        self.vlayout2.setAlignment(Qt.AlignTop)
        self.vlayout2.setSpacing(10)

        # Element count
        label = QLabel()
        label.setText("Amount of Elements")
        self.vlayout2.addWidget(label)

        self.element_count_input = QComboBox(self)
        self.element_count_input.setMinimumWidth(150)
        powers_of_two = [str(2**x) for x in range(3, 12)]
        self.element_count_input.addItems(powers_of_two)
        self.element_count_input.setCurrentText("64")
        self.vlayout2.addWidget(self.element_count_input)

        # Rendering style
        label = QLabel()
        label.setText("Rendering style")
        self.vlayout2.addWidget(label)

        self.rendering_input = QComboBox(self)
        self.rendering_input.setMinimumWidth(150)
        self.rendering_input.addItems(["Bar Graph", "Point Graph", "Point Spiral", "Point Circle"])
        self.vlayout2.addWidget(self.rendering_input)

        self.linear_checkbox = QCheckBox()
        self.linear_checkbox.setText("Shuffle Linear Elements")
        self.linear_checkbox.setChecked(True)
        self.linear_checkbox.setStyleSheet("QCheckBox::indicator::unchecked { border-radius:5px; border-style: solid; border-width:1px; border-color: gray;}")
        self.vlayout2.addWidget(self.linear_checkbox)

        self.color_checkbox = QCheckBox()
        self.color_checkbox.setText("Rainbow Coloring")
        self.color_checkbox.setStyleSheet("QCheckBox::indicator::unchecked { border-radius:5px; border-style: solid; border-width:1px; border-color: gray;}")
        self.vlayout2.addWidget(self.color_checkbox)
        

        self.hlayout.addLayout(self.vlayout2)

        self.hlayout.addStretch(1)
        self.layout.addSpacing(20)

        start_button = QPushButton(self)
        start_button.setText("Start Sorting")
        start_button.setMaximumWidth(390)
        start_button.setMinimumWidth(300)
        start_button.clicked.connect(self.startSorting)

        self.layout.addWidget(start_button, Qt.AlignCenter)
        self.layout.addStretch(1)

    def startSorting(self):

        # Generate list based on options
        lst = special_types.SList()
        element_count = int(self.element_count_input.currentText())
        if self.linear_checkbox.isChecked():
            lst.shuffle_linear(element_count)
        else:
            lst.randomize(element_count, element_count)

        # Other attributes
        rendering_types_map = {"Bar Graph": SortRenderType.BarGraph, "Point Graph": SortRenderType.PointGraph, 
            "Point Spiral": SortRenderType.PointSpiral, "Point Circle": SortRenderType.PointCircle}

        rainbow = self.color_checkbox.isChecked()
        rendering_type = rendering_types_map[self.rendering_input.currentText()]

        # Convert dropdown names to Sorting Algorithm objects. Filter out "None" options
        algo_names = filter(lambda a: a != "None", [dropdown.currentText() for dropdown in self.sorting_selections])
        sorting_algos = [SortingAlgorithm(self.sorting_func_map[name], name, lst) for name in algo_names]
        self.main_window.switchToSorting(sorting_algos, element_count, rendering_type, rainbow)

class MainWindow(QWidget):
    def __init__(self, sorting_func_map):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Sorting Algorithms Visualized')
        self.setStyleSheet("background-color: #181818; color: white")

        # Setup custom font
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("../assets/fonts/Inter-Regular.ttf")

        # Setup window tabs
        self.tabs = QStackedWidget(self)
        self.selection_tab = SelectionTab(self.tabs, sorting_func_map, self)
        self.sorting_tab = SortingTab(self.tabs)

        self.tabs.addWidget(self.selection_tab)
        self.tabs.addWidget(self.sorting_tab)

        self.tabs.setCurrentIndex(0)
        self.tabs.currentWidget().setFocus()

        self.resize(400, 380)
        #self.selection_tab.resize(400, 380)

    def switchToSorting(self, sorting_algos, element_count, rendering_type, rainbow):
        count = max(1, len(sorting_algos))
        self.resize(430 * min(4, count), 430 * min(2, (count-1)//4 + 1))
        self.tabs.resize(430 * min(4, count), 430 * min(2, (count-1)//4 + 1))
        self.tabs.setCurrentIndex(1)
        self.sorting_tab.rendering_type = rendering_type
        self.sorting_tab.rainbow = rainbow
        self.sorting_tab.updateSortingAlgorithms(sorting_algos)
        self.sorting_tab.startRendering()

class MainApplication(QApplication):
    def __init__(self, sorting_func_map):
        super().__init__([])

        window = MainWindow(sorting_func_map)
        window.show()

        sys.exit(self.exec_())