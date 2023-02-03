import sys
from random import choice
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong'
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_times_clicked = 0

        self.setWindowTitle("My GUI")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.button_click)

        self.windowTitleChanged.connect(self.window_title_change)

        # Set the central widget of the Window.
        self.setCentralWidget(self.button)

    def button_click(self):
        print("Clicked!")
        new_window_title = choice(window_titles)
        print("Setting title:  %s" % new_window_title)
        self.setWindowTitle(new_window_title)

    def window_title_change(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == 'Something went wrong':
            self.button.setDisabled(True)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
