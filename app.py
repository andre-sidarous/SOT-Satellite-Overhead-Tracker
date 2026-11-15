from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMenu, QWidget, QMainWindow, QToolBar, QLabel, QMenu, QTabWidget
from PyQt6.QtGui import QIcon
import sys

app = QApplication(sys.argv)

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
                width: 150px;
                height: 40px;
                margin: 2px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #3d3938;
            }
            QTabBar::tab:selected {
                background-color: #3d3938;
            }
        """)
        tabs.addTab(QLabel("Content of Tab 1"),QIcon("3413124.png"), "Tab 1")
        tabs.addTab(QLabel("Content of Tab 2"),QIcon("3413124.png"), "Tab 2")

        self.setCentralWidget(tabs)
window = MainWindow()
window.show()

app.exec()