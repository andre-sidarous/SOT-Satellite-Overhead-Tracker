from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMenu, QWidget, QMainWindow, QToolBar, QLabel, QMenu, QTabWidget, QListWidget, QGridLayout
from PyQt6.QtGui import QIcon
import sys

app = QApplication(sys.argv)

coordinates = {"Kennedy Space Center": (28.6, -80.7), "Marshall Space Flight Center": (34.6, -86.7), "Johnson Space Center": (29.6, -95.1), "Stennis Space Center": (30.4, -89.6)}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MECEarth")
        self.width, self.height = 800, 600
        self.setFixedSize(QSize(self.width, self.height))

        mission_control = Label("Mission Control", 30)
        locations_list = CheckList(coordinates)

        layout = GridLayout(
                    [[mission_control],
                    [locations_list]]
                )
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(False)
        tabs.setStyleSheet("""
            QTabBar::tab {
                width: 100px;
                height: 200px;
                margin: 2px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #3d3938;
            }
            QTabBar::tab:selected {
                background-color: #635c5a;
            }
        """)
        tabs.addTab(QLabel("Hello, welcome to MECEarth!"),QIcon("3413124.png"), "Menu")
        tabs.addTab((container), QIcon("3413124.png"), "Tab 2")
        tabs.setIconSize(QSize(100, 100))

        self.setCentralWidget(tabs)

class GridLayout(QGridLayout):
    def __init__(self, layout: List[List[QWidget]]):
        super().__init__()

        max_width = 0

        for row in layout:
            if len(row) > max_width:
                max_width = len(row)

        for i in range(len(layout)):
            for j in range(max_width):
                if j < max_width:
                    self.addWidget(layout[i][j], i, j)

class CheckList(QListWidget):
    def __init__(self, items):
        super().__init__()

        self.items = items

        for name in items:
            self.addItem(name)

        self.current = None

        self.currentItemChanged.connect(self.index_changed)

    def index_changed(self, listItem):
        self.current = listItem.text()

    def get_coordinates(self):
        if not self.current:
            return None # TODO

        return self.items[self.current]

class Label(QLabel):
    def __init__(self, text: str, font_size: int):
        super().__init__(text)

        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)

        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

window = MainWindow()
window.show()


app.exec()