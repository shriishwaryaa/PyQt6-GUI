import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My GUI")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.button_click)
        button.clicked.connect(self.button_toggle)

        # Set the central widget of the Window.
        self.setCentralWidget(button)

    def button_click(self):
        print("Clicked!")

    def button_toggle(self, checked):
        print("Checked?", checked)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
