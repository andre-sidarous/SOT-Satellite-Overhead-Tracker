from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width, self.height = 800, 600

        self.setFixedSize(self.width, self.height)

        layout = GridLayout()

        container = QWidget()
        container.setLayout(layout)

class GridLayout(QGridLayout):
    def __init__(self):
        super().__init__()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()