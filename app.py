from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mecearth")
        self.width, self.height = 800, 600
        self.setFixedSize(QSize(self.width, self.height))

        label = Label("Welcome to Mission Control!", 30)
        self.setCentralWidget(label)

class Label(QLabel):
    def __init__(self, text: str, font_size: int):
        super().__init__(text)

        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)

        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()