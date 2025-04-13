import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer
class DA(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.radius = 200
        self.center = (300, 300)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(100)
    def update_position(self):
        self.angle = (self.angle + 5) % 360
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setPen(QColor(0, 0, 0))
        painter.drawEllipse(self.center[0] - self.radius, self.center[1] - self.radius, self.radius * 2, self.radius * 2)

        x = int(self.center[0] + self.radius * math.cos(math.radians(self.angle)))
        y = int(self.center[1] + self.radius * math.sin(math.radians(self.angle)))

        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(x - 10, y - 10, 20, 20)
class Okno(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Безуглов И.В. - 1 лаба")
        self.setFixedSize(600, 600)
        self.drawing_area = DA()
        self.setCentralWidget(self.drawing_area)
app = QApplication(sys.argv)
window = Okno()
window.show()
app.exec()
