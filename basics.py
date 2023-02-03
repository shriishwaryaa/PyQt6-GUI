from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My GUI")
        button = QPushButton("Press Me!")

        self.setMinimumSize(QSize(500, 300))
        self.setMaximumSize(QSize(700, 500))

        # Set the central widget of the Window
        self.setCentralWidget(button)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
