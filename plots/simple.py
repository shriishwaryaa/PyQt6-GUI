import sys
import matplotlib
matplotlib.use('QtAgg')

from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My GUI")

        plot = MplCanvas(self, width=5, height=4, dpi=100)
        plot.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        toolbar = NavigationToolbar2QT(plot, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(plot)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
