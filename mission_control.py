from typing import Dict, List
from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QSizePolicy, QWidget, QListWidget, QLineEdit, QPushButton
from PyQt6.QtGui import QFontMetrics
from parse_coords import parse_coords
from seeIfCollisions import seeIfCollision
from getSatelliteLocations import getSatelliteLocations

class MainWindow(QMainWindow):
    width, height = 800, 600
    big_size, medium_size, small_size, tiny_size = 30, 25, 15, 8

    def __init__(self):
        super().__init__()
        self.setWindowTitle("mecearth")
        self.setFixedSize(QSize(self.width, self.height))

        mission_control = Label(
            "Mission Control",
            self.big_size,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        location = Label(
            "Location",
            self.medium_size,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        instructions1 = Label(
            "Select a space center:",
            self.small_size,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        self.locations_list = CheckList(
            {"Enter coordinates manually": None, "Tokyo": (0,0), "Toronto":(1,1), "Paris":(2,2)},
            lambda: self.error_coordinates.setText("")
        )
        instructions2 = Label(
            "or enter coordinates randomly:",
            self.small_size,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        self.coordinates_input = LineInput(
            "Coordinates: Latitude, Longitude",
            lambda: self.error_coordinates.setText("")
        )
        self.error_coordinates = errorMessage()

        parameters = Label(
            "Parameters",
            self.medium_size,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        self.max_elevation = LineInput(
            "Enter max elevation (m):",
            lambda: self.error_max_elevation.setText("")
        )
        self.error_max_elevation = errorMessage()

        self.max_variance_longitude = LineInput(
            "Enter max variance in longitude (Default 0.5):",
            lambda: self.error_max_variance_longitude.setText("")
        )
        self.max_variance_latitude = LineInput(
            "Enter max variance in longitude (Default 0.25):",
            lambda: self.error_max_variance_latitude.setText("")
        )

        self.button = QPushButton("Run Calculations")
        self.button.pressed.connect(self.submit)

        mission_dashboard = Label(
            "Mission Dashboard",
            self.big_size,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        self.result = Label(
            "No Data Submitted",
            self.small_size,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        self.result.setWordWrap(True)
        self.result.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.result.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.crash_state = Label(
            "",
            self.medium_size,
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter
        )

        self.layout = GridLayout(
            [
            [mission_control, mission_dashboard],
            [location, self.crash_state],
            [instructions1, self.result],
            [self.locations_list],
            [instructions2],
            [self.coordinates_input],
            [self.error_coordinates.label],
            [parameters],
            [self.max_elevation],
            [self.error_max_elevation.label],
            [self.max_variance_longitude],
            [self.max_variance_latitude],
            [self.button]
            ]
        )

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def invalid_coordinates(self):
        self.error_coordinates.setText("Invalid coordinates or invalid format: Latitude, Longitude")

    def get_coordinates(self):
        coordinates = None
        
        coordinates = self.locations_list.get_coordinates()
        if coordinates:
            return coordinates

        return parse_coords(self.coordinates_input.text)

    def get_output(self, latitude, max_variance_latitude, longitude, max_variance_longitude, max_elevation):
        satelliteDict = getSatelliteLocations()
        satelliteCollisions = seeIfCollision(
            latitude,
            max_variance_latitude,
            longitude,
            max_variance_longitude,
            satelliteDict,
            max_elevation
        )
        
        if not satelliteCollisions:
            return ("A satellite launched from this point on Earth would not collide with any satellites.", False)

        text = "A satellite launched from this point on Earth would collide with the following satellites:\n"
        for satellite in satelliteCollisions[:-1]:
            text += satellite + ", "
        text += satelliteCollisions[-1] + "."

        return (text, True)

    def submit(self):
        coordinates = self.get_coordinates()
        if not coordinates:
            self.error_coordinates.setText("Please choose a space center or enter coordinates.")
            return

        try:
            max_elevation = float(self.max_elevation.text)
        except:
            self.error_max_elevation.setText("Please enter a decimal number for elevation.")
            return

        try:
            max_variance_longitude = float(self.max_variance_longitude.text)
        except:
            max_variance_longitude = 0.5

        try:
            max_variance_latitude = float(self.max_variance_latitude.text)
        except:
            max_variance_latitude = 0.25

        latitude, longitude = coordinates

        (output_text, has_crashed) = self.get_output(
            latitude,
            max_variance_latitude,
            longitude,
            max_variance_longitude,
            max_elevation
        )

        color = ""
        if has_crashed:
            color = "red"
            self.crash_state.setText("YOUR CRAFT WILL COLLIDE")
        else:
            color = "green"
            self.crash_state.setText("YOUR CRAFT IS SAFE")

        self.crash_state.setStyleSheet(f"background-color: {color}; color: white; padding: 4px;")
        self.crash_state.setAutoFillBackground(True)

        self.result.setText(output_text)
        self.result.fit_font()

class LineInput(QLineEdit):
    text = ""
    coordinates = None

    def __init__(self, placeholder: str, lambda_text_changed = None):
        super().__init__()

        self.placeholder = placeholder
        self.lambda_text_changed = lambda_text_changed

        self.setPlaceholderText(self.placeholder)

        self.textChanged.connect(self.text_changed)

    def text_changed(self, text: str):
        self.text = text

        if self.lambda_text_changed:
            self.lambda_text_changed()

class GridLayout(QGridLayout):
    def __init__(self, items: List[List[QWidget]]):
        super().__init__()

        max_width = 0

        for row in items:
            if len(row) > max_width:
                max_width = len(row)

        for i in range(len(items)):
            for j in range(max_width):
                if j < len(items[i]):
                    self.addWidget(items[i][j], i, j)

        for r in range(len(items)):
            self.setRowStretch(r, 1)
        for c in range(max_width):
            self.setColumnStretch(c, 1)

class CheckList(QListWidget):
    def __init__(self, items: Dict, lambda_index_changed = None):
        super().__init__()

        self.lambda_index_changed = lambda_index_changed

        self.items = items

        for name in items:
            self.addItem(name)

        self.current = None
        self.count = 0
        self.currentItemChanged.connect(self.index_changed)

    def index_changed(self, listItem):
        self.current = listItem.text()
        if self.lambda_index_changed:
            self.lambda_index_changed()

    def get_coordinates(self):
        if not self.current:
            return None

        return self.items[self.current]

class Label(QLabel):
    def __init__(self, text: str, font_size: int, alignment):
        super().__init__(text)

        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)

        self.setAlignment(alignment)

    def fit_font(self, max_pt=32, min_pt=6):
        rect = self.contentsRect()
        if rect.width() <= 0 or rect.height() <= 0:
            return
        flags = int(Qt.TextFlag.TextWordWrap | Qt.AlignmentFlag.AlignCenter)

        lo, hi, best = min_pt, max_pt, min_pt
        while lo <= hi:                          # binary search for the largest size that fits
            mid = (lo + hi) // 2
            font = self.font()
            font.setPointSize(mid)
            bounds = QFontMetrics(font).boundingRect(
                QRect(0, 0, rect.width(), 100_000), flags, self.text()
            )
            if bounds.height() <= rect.height():
                best, lo = mid, mid + 1
            else:
                hi = mid - 1

        font = self.font()
        font.setPointSize(best)
        self.setFont(font)

class errorMessage():
    def __init__(self):
        self.label = Label(
            "",
            15,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
    def setText(self, text: str):
        self.label.setText(text)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()