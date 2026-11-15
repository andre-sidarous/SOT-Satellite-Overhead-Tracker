from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMenu, QWidget, QMainWindow, QToolBar, QLabel, QMenu, QTabWidget
from PyQt6.QtGui import QIcon
import sys

app = QApplication(sys.argv)

coordinates = {"kennedy_space_center": (28.573469, -80.651070), "marshall_space_flight_center": (34.6458874, -86.6756394), "johnson_space_center": (29.559303, -95.090062), "stennis_space_center": (30.362778, -89.600278)}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.resize(QSize(800, 600))
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
        tabs.addTab(QLabel("Content of Tab 2"),QIcon("3413124.png"), "Tab 2")
        tabs.setIconSize(QSize(100, 100))

        self.setCentralWidget(tabs)
window = MainWindow()
window.show()

app.exec()