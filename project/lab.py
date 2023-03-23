import time
import serial
import matplotlib
import serial.tools.list_ports
matplotlib.use('QtAgg')

from PyQt6 import QtCore
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QSpinBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MotorInput(QWidget):
    def __init__(self, name, minimum, maximum, step, suffix, options, needed, color):
        super(MotorInput, self).__init__()

        self.label = QLabel(name)
        self.value = QSpinBox()
        self.value.setMinimum(minimum)
        self.value.setMaximum(maximum)
        self.value.setSingleStep(step)
        self.value.setSuffix(suffix)
        self.button = QPushButton("Enter")

        self.valueStored = 0

        self.setAutoFillBackground(True)
        r, g, b, t = color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(r, g, b, t))
        self.setPalette(palette)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.value)

        if needed == 1:
            self.dropdown = QComboBox()
            self.dropdown.addItems(options)
            self.optionChosen = 0
            layout.addWidget(self.dropdown)

        layout.addWidget(self.button)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, ser):
        super().__init__()

        self.ser = serial.Serial(ser, 9600, timeout=1)
        self.states = {"U": 0, "BUSt": 1, "St": 3, "DC": 4, "Se": 5, "F": 6, "O": 7, "IR": 8}
        self.dropdownToState = {0: 0, 1: 3, 2: 1, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}
        self.stateChosen = 0
        self.time = time.time()

        self.setWindowTitle("My GUI")

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        self.state = 0
        self.xdata = []
        self.ydata = []

        self._plot_ref = None
        self.update_plot()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.dc = MotorInput("DC motor :", -360, 360, 1, " Degree", ["Position control", "Velocity control"], 1, (255, 153, 153, 125))
        self.dc.value.valueChanged.connect(self.dc_value_change)
        self.dc.button.clicked.connect(self.dc_button_click)
        self.dc.dropdown.currentIndexChanged.connect(self.dc_index_change)

        self.stepper = MotorInput("Stepper motor :", 0, 359, 1, " Degree", ["Anti-clockwise", "Clockwise"], 1, (153, 255, 204, 125))
        self.stepper.value.valueChanged.connect(self.stepper_value_change)
        self.stepper.button.clicked.connect(self.stepper_button_click)
        self.stepper.dropdown.currentIndexChanged.connect(self.stepper_index_change)

        self.servo = MotorInput("Servo motor :", 0, 202, 1, " Degree", [], 0, (153, 204, 255, 125))
        self.servo.value.valueChanged.connect(self.servo_value_change)
        self.servo.button.clicked.connect(self.servo_button_click)

        self.omron = QLabel("Count: 0")
        self.omron.setAutoFillBackground(True)
        palette = self.omron.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 0, 125))
        self.omron.setPalette(palette)
        self.omron.setContentsMargins(10, 0, 0, 0)

        self.currentState = QComboBox()
        self.currentState.addItems(["Ultrasonic sensor", "Stepper motor", "Ultrasonic + Stepper", "DC motor",
                                    "Servo motor", "Force sensor", "Omron sensor", "IR sensor"])
        self.currentState.currentIndexChanged.connect(self.state_change)

        self.stepper.setEnabled(False)
        self.dc.setEnabled(False)
        self.servo.setEnabled(False)
        self.omron.setEnabled(False)

        layout1 = QVBoxLayout()
        layout1.addWidget(self.dc)
        layout1.addWidget(self.stepper)
        layout1.addWidget(self.servo)
        layout1.addWidget(self.omron)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.currentState)
        layout2.addWidget(self.canvas)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(layout1)
        mainLayout.addLayout(layout2)

        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setFixedSize(1300, 700)
        self.setContentsMargins(0, 160, 0, 160)
        self.setCentralWidget(widget)

        serialOutput = str(0) + str(self.stepper.optionChosen) + str(self.stepper.valueStored)
        self.ser.write(serialOutput.encode())

    def update_plot(self):
        text = self.ser.readline().decode().split()
        if len(text) > 0:
            y = float(text[0])

            if self.stateChosen in [0, 5, 7]:
                x = float(time.time() - self.time)

                if len(self.ydata) > 15:
                    self.ydata = self.ydata[1:] + [y]
                    self.xdata = self.xdata[1:] + [x]
                    xLower = float(min(self.xdata))
                    xUpper = float(max(self.xdata))
                    yLower = float(min(self.ydata))
                    yUpper = float(max(self.ydata))
                else:
                    self.ydata = self.ydata + [y]
                    self.xdata = self.xdata + [x]
                    xLower = float(min(self.xdata)) - 2
                    xUpper = float(max(self.xdata)) + 2
                    yLower = float(min(self.ydata)) - 10
                    yUpper = float(max(self.ydata)) + 10

                # print(self.ydata)
                # print(self.xdata)

                if self._plot_ref is None:
                    plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
                    self._plot_ref = plot_refs[0]
                else:
                    self._plot_ref.set_xdata(self.xdata)
                    self._plot_ref.set_ydata(self.ydata)
                    self.canvas.axes.set_xlim([xLower, xUpper])
                    self.canvas.axes.set_ylim([yLower, yUpper])

                self.canvas.draw()

            if self.stateChosen == 6:
                self.omron.setText("Count: %s" % str(int(y)))

    def dc_value_change(self, i):
        self.dc.valueStored = i

    def dc_button_click(self):
        text = "Degree" if self.dc.optionChosen == 0 else "RPM"
        print("DC value : %s %s" % (self.dc.valueStored, text))
        serialOutput = str(self.states["DC"]) + str(self.dc.optionChosen) + str(self.dc.valueStored)
        self.ser.write(serialOutput.encode())

    def dc_index_change(self, i):
        self.dc.optionChosen = i
        self.dc.value.setSuffix(" Degree") if self.dc.optionChosen == 0 else self.dc.value.setSuffix(" RPM")
        self.dc.value.setRange(-360, 360) if self.dc.optionChosen == 0 else self.dc.value.setRange(-60, 60)

    def stepper_value_change(self, i):
        self.stepper.valueStored = i

    def stepper_button_click(self):
        text = "Clockwise" if self.stepper.optionChosen == 0 else "Anti-clockwise"
        print("Stepper value : %s %s" % (self.stepper.valueStored, text))
        serialOutput = str(self.states["St"]) + str(self.stepper.optionChosen) + str(self.stepper.valueStored)
        self.ser.write(serialOutput.encode())

    def stepper_index_change(self, i):
        self.stepper.optionChosen = i

    def servo_value_change(self, i):
        self.servo.valueStored = i

    def servo_button_click(self):
        print("Servo value : %s %s" % (self.servo.valueStored, "Degree"))
        serialOutput = str(self.states["Se"]) + str(0) + str(self.servo.valueStored)
        self.ser.write(serialOutput.encode())

    def state_change(self, i):
        self.stateChosen = i
        print(self.stateChosen)

        self.ser.flushInput()
        self.xdata = []
        self.ydata = []
        self.canvas.axes.cla()
        self._plot_ref = None
        self.time = time.time()

        serialOutput = str(self.dropdownToState[self.stateChosen]) + str(0) + str(self.servo.valueStored)
        self.ser.write(serialOutput.encode())

        if self.stateChosen in [0, 2, 5, 7]:
            self.stepper.setEnabled(False)
            self.dc.setEnabled(False)
            self.servo.setEnabled(False)
            self.omron.setEnabled(False)
        elif self.stateChosen == 1:
            self.stepper.setEnabled(True)
            self.dc.setEnabled(False)
            self.servo.setEnabled(False)
            self.omron.setEnabled(False)
        elif self.stateChosen == 3:
            self.stepper.setEnabled(False)
            self.dc.setEnabled(True)
            self.servo.setEnabled(False)
            self.omron.setEnabled(False)
        elif self.stateChosen == 4:
            self.stepper.setEnabled(False)
            self.dc.setEnabled(False)
            self.servo.setEnabled(True)
            self.omron.setEnabled(False)
        elif self.stateChosen == 6:
            self.omron.setEnabled(True)


def arduinoPort():
    ports = list(serial.tools.list_ports.comports())

    resultPorts = []
    descriptions = []
    for port in ports:
        if "n/a" not in port:
            return str(port).split(" ")[0]

        if not port.description.startswith("Arduino"):
            if port.manufacturer is not None:
                if port.manufacturer.startswith("Arduino") and \
                   port.device.endswith(port.description):
                    port.description = "Arduino Uno"
                else:
                    continue
            else:
                continue
        if port.device:
            resultPorts.append(port.device)
            descriptions.append(str(port.description))

    for i in descriptions:
        if "Arduino" in i:
            return port[descriptions.index(i)]


serialPort = arduinoPort()
print(serialPort)

app = QApplication([])

window = MainWindow(serialPort)
window.show()

app.exec()



