from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTabWidget
from PyQt6.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        self.setFixedSize(QSize(800, 600))

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(False)
        tabs.setStyleSheet()
        tabs.addTab(QLabel("Content of Tab 1"),QIcon("3413124.png"), "Tab 1")
        tabs.addTab(QLabel("Content of Tab 2"),QIcon("3413124.png"), "Tab 2")

        self.setCentralWidget(tabs)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()