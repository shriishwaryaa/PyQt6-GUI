from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My GUI")
        button = QPushButton("Press Me!")

        # Set the central widget of the Window
        self.setCentralWidget(button)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
