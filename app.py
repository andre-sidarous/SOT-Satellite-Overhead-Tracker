from typing import List
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QListWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mecearth")
        self.width, self.height = 800, 600
        self.setFixedSize(QSize(self.width, self.height))

        mission_control = Label("Mission Control", 30)
        locations_list = CheckList(["Tokyo", "Toronto", "Paris"])

        layout = GridLayout(
            [[mission_control],
            [locations_list]]
        )

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

class GridLayout(QGridLayout):
    def __init__(self, layout: List[QWidget]):
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
    def __init__(self, items: List[str]):
        super().__init__()

        self.addItems(items)

        self.current = None

        self.currentItemChanged.connect(self.index_changed)

    def index_changed(self, listItem):
        self.current = listItem.text()

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