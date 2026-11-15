import math
import sys
from typing import Callable, Dict, Optional, Tuple

from PyQt6.QtCore import QRect, QSize, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFontMetrics, QIcon, QMovie
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from getSatelliteLocations import getSatelliteLocations
from parse_coords import parse_coords
from seeIfCollisions import seeIfCollision

# ---------------------------------------------------------------- constants

SPACE_CENTERS = {
    "Kennedy Space Center": (28.6, -80.7),
    "Marshall Space Flight Center": (34.6, -86.7),
    "Johnson Space Center": (29.6, -95.1),
    "Stennis Space Center": (30.4, -89.6),
}
MANUAL_ENTRY = "Enter coordinates manually"

DEFAULT_VARIANCE_LATITUDE = 0.25
DEFAULT_VARIANCE_LONGITUDE = 0.5

WINDOW_SIZE = QSize(1100, 700)
BIG_SIZE, MEDIUM_SIZE, SMALL_SIZE = 30, 25, 15

CENTER = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
LEFT = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft

TAB_STYLE = """
    QTabBar::tab {
        width: 200px;
        height: 60px;
        margin: 3px;
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #3d3938;
        font-size: 32px;
        font-weight: bold;
    }
    QTabBar::tab:selected {
        background-color: #635c5a;
    }
"""


# ---------------------------------------------------------- background work

class CalculationThread(QThread):
    """Runs the slow satellite lookup off the UI thread."""

    finished_calculating = pyqtSignal(str, bool)  # (result text, will_collide)
    failed = pyqtSignal(str)                      # error message

    def __init__(self, latitude, longitude, max_variance_latitude,
                 max_variance_longitude, max_elevation):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.max_variance_latitude = max_variance_latitude
        self.max_variance_longitude = max_variance_longitude
        self.max_elevation = max_elevation

    def run(self):
        try:
            satellite_dict = getSatelliteLocations()
            collisions = seeIfCollision(
                self.latitude,
                self.max_variance_latitude,
                self.longitude,
                self.max_variance_longitude,
                satellite_dict,
                self.max_elevation,
            )
        except Exception as error:  # network errors, bad data, etc.
            self.failed.emit(f"Calculation failed: {error}")
            return

        if not collisions:
            self.finished_calculating.emit(
                "A satellite launched from this point on Earth would not "
                "collide with any satellites.",
                False,
            )
        else:
            self.finished_calculating.emit(
                "A satellite launched from this point on Earth would collide "
                "with the following satellites:\n"
                + ", ".join(str(name) for name in collisions) + ".",
                True,
            )


# -------------------------------------------------------------- main window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MECEarth")
        self.setFixedSize(WINDOW_SIZE)

        self.worker: Optional[CalculationThread] = None

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(False)
        tabs.setStyleSheet(TAB_STYLE)
        tabs.setIconSize(QSize(60, 60))

        tabs.addTab(
            Label("Hello, welcome to MECEarth!", 50, CENTER),
            QIcon("3413124.png"),
            "Menu",
        )
        tabs.addTab(self.build_launch_tab(), QIcon("rocket.png"), "Launch")

        self.setCentralWidget(tabs)

    # ---- layout

    def build_launch_tab(self) -> QWidget:
        # Left column: inputs
        self.locations_list = CheckList(
            {MANUAL_ENTRY: None, **SPACE_CENTERS},
            self.clear_coordinate_error,
        )
        self.coordinates_input = LineInput(
            "Coordinates: Latitude, Longitude",
            self.clear_coordinate_error,
        )
        self.error_coordinates = ErrorLabel()

        self.max_elevation = LineInput(
            "Enter max elevation (m):",
            self.clear_parameter_error,
        )
        self.max_variance_longitude = LineInput(
            f"Enter max variance in longitude (Default {DEFAULT_VARIANCE_LONGITUDE}):",
            self.clear_parameter_error,
        )
        self.max_variance_latitude = LineInput(
            f"Enter max variance in latitude (Default {DEFAULT_VARIANCE_LATITUDE}):",
            self.clear_parameter_error,
        )
        self.error_parameters = ErrorLabel()

        self.button = QPushButton("Run Calculations")
        self.button.clicked.connect(self.submit)

        left = QVBoxLayout()
        for widget in (
            Label("Mission Control", BIG_SIZE, CENTER),
            Label("Location", MEDIUM_SIZE, LEFT),
            Label("Select a space center:", SMALL_SIZE, LEFT),
            self.locations_list,
            Label("or enter coordinates manually:", SMALL_SIZE, LEFT),
            self.coordinates_input,
            self.error_coordinates,
            Label("Parameters", MEDIUM_SIZE, LEFT),
            self.max_elevation,
            self.max_variance_longitude,
            self.max_variance_latitude,
            self.error_parameters,
            self.button,
        ):
            left.addWidget(widget)

        # Right column: results
        self.crash_state = Label("", MEDIUM_SIZE, CENTER)

        self.result = Label(
            "No Data Submitted",
            MEDIUM_SIZE,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )
        self.result.setWordWrap(True)
        self.result.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.result.setMinimumSize(100, 70)

        self.movie = QMovie("gear.gif")
        self.movie.setScaledSize(QSize(60, 60))

        right = QVBoxLayout()
        right.addWidget(Label("Mission Dashboard", BIG_SIZE, CENTER))
        right.addWidget(self.crash_state)
        right.addWidget(self.result, stretch=1)  # result gets all spare height

        row = QHBoxLayout()
        row.addLayout(left, 1)
        row.addLayout(right, 1)

        container = QWidget()
        container.setLayout(row)
        return container

    # ---- error helpers

    def clear_coordinate_error(self):
        self.error_coordinates.setText("")

    def clear_parameter_error(self):
        self.error_parameters.setText("")

    # ---- input reading

    def get_coordinates(self) -> Optional[Tuple[float, float]]:
        """Returns (lat, lon), or None after showing an error."""
        selected = self.locations_list.get_coordinates()
        if selected is not None:
            return selected

        text = self.coordinates_input.text().strip()
        if not text:
            self.error_coordinates.setText("Please choose a space center or enter coordinates.")
            return None

        try:
            latitude, longitude = (float(v) for v in parse_coords(text))
        except Exception:  # parse_coords returned None, wrong shape, or raised
            self.error_coordinates.setText(
                "Invalid coordinates or invalid format: Latitude, Longitude"
            )
            return None

        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            self.error_coordinates.setText(
                "Latitude must be in [-90, 90] and longitude in [-180, 180]."
            )
            return None

        return latitude, longitude

    def get_parameters(self) -> Optional[Tuple[float, float, float]]:
        """Returns (max_elevation, var_lat, var_lon), or None after showing an error."""
        try:
            max_elevation = read_float(self.max_elevation)
            var_lon = read_float(self.max_variance_longitude, DEFAULT_VARIANCE_LONGITUDE)
            var_lat = read_float(self.max_variance_latitude, DEFAULT_VARIANCE_LATITUDE)
        except ValueError:
            self.error_parameters.setText("Parameters must be decimal numbers.")
            return None

        if max_elevation is None:
            self.error_parameters.setText("Please enter a max elevation (m).")
            return None

        if not all(math.isfinite(v) and v > 0 for v in (max_elevation, var_lon, var_lat)):
            self.error_parameters.setText("Elevation and variances must be positive numbers.")
            return None

        return max_elevation, var_lat, var_lon

    # ---- actions

    def submit(self):
        coordinates = self.get_coordinates()
        parameters = self.get_parameters()  # run both so both errors can show
        if coordinates is None or parameters is None:
            return

        latitude, longitude = coordinates
        max_elevation, var_lat, var_lon = parameters

        self.start_loading()

        self.worker = CalculationThread(latitude, longitude, var_lat, var_lon, max_elevation)
        self.worker.finished_calculating.connect(self.display_result)
        self.worker.failed.connect(self.display_error)
        self.worker.start()

    def start_loading(self):
        self.button.setEnabled(False)
        self.set_crash_state(None)
        self.result.clear()
        if self.movie.isValid():
            self.result.setMovie(self.movie)
            self.movie.start()
        else:  # gear.gif missing: fall back to text
            self.result.setText("Calculating...")

    def stop_loading(self, text: str):
        self.movie.stop()
        self.result.clear()  # also removes the movie
        self.result.setText(text)
        self.result.fit_font()
        self.button.setEnabled(True)

    def display_result(self, text: str, will_collide: bool):
        self.set_crash_state(will_collide)
        self.stop_loading(text)

    def display_error(self, message: str):
        self.set_crash_state(None)
        self.stop_loading(message)

    def set_crash_state(self, will_collide: Optional[bool]):
        if will_collide is None:
            self.crash_state.setText("")
            self.crash_state.setStyleSheet("")
            return
        color = "red" if will_collide else "green"
        self.crash_state.setText("YOUR CRAFT WILL COLLIDE" if will_collide else "YOUR CRAFT IS SAFE")
        self.crash_state.setStyleSheet(f"background-color: {color}; color: white; padding: 4px;")

    def closeEvent(self, event):
        # Destroying a QThread while it runs crashes the app.
        if self.worker is not None and self.worker.isRunning():
            self.worker.wait()
        super().closeEvent(event)


# ------------------------------------------------------------------ widgets

def read_float(line_edit: QLineEdit, default: Optional[float] = None) -> Optional[float]:
    """Empty -> default. Otherwise float(text), raising ValueError if invalid."""
    text = line_edit.text().strip()
    if not text:
        return default
    return float(text)


class LineInput(QLineEdit):
    def __init__(self, placeholder: str, on_change: Optional[Callable[[], None]] = None):
        super().__init__()
        self.setPlaceholderText(placeholder)
        if on_change:
            self.textChanged.connect(lambda _text: on_change())


class CheckList(QListWidget):
    def __init__(self, options: Dict[str, Optional[Tuple[float, float]]],
                 on_change: Optional[Callable[[], None]] = None):
        super().__init__()
        self.options = options
        self.current: Optional[str] = None
        self.on_change = on_change

        self.addItems(list(options))
        self.currentItemChanged.connect(self.index_changed)

    def index_changed(self, item, _previous):
        self.current = item.text() if item is not None else None
        if self.on_change:
            self.on_change()

    def get_coordinates(self) -> Optional[Tuple[float, float]]:
        if self.current is None:
            return None
        return self.options[self.current]


class Label(QLabel):
    def __init__(self, text: str, font_size: int, alignment):
        super().__init__(text)
        font = self.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(alignment)

    def fit_font(self, max_pt: int = 32, min_pt: int = 6):
        """Binary-search the largest font size whose wrapped text fits the label."""
        rect = self.contentsRect()
        if rect.width() <= 0 or rect.height() <= 0:
            return
        flags = Qt.TextFlag.TextWordWrap.value | Qt.AlignmentFlag.AlignCenter.value

        lo, hi, best = min_pt, max_pt, min_pt
        while lo <= hi:
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


class ErrorLabel(Label):
    def __init__(self):
        super().__init__("", SMALL_SIZE, LEFT)
        self.setStyleSheet("color: #e05050;")


# --------------------------------------------------------------------- main

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())