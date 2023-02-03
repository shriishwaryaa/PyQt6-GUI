import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My GUI")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.button_click)

        # Set the central widget of the Window.
        self.setCentralWidget(self.button)

    def button_click(self):
        self.button.setText("You already pressed me!")
        self.button.setEnabled(False)

        self.setWindowTitle("My GUI changes")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
