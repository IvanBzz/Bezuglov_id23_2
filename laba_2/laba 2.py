from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer, QPoint
import sys
import numpy as np
import time

class Planets(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_time = time.time()  #время начала анимации
        self.initial_angles = [np.random.uniform(0, 360) for _ in range(8)]
    def initUI(self):  # метод для установки параметров окна
        self.setWindowTitle("Bezuglov laba 2")
        self.setGeometry(200, 100, 800, 600)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))  # черный цвет
        painter.setBrush(QColor(0, 0, 0))  # черный цвет
        painter.drawRect(0, 0, 800, 600)#Фон
        #Солнце
        painter.setPen(QColor(255, 255, 0, 200))
        painter.setBrush(QColor(255, 255, 0, 200))
        painter.drawEllipse(QPoint(400, 300), 60, 60)
        elapsed_time = abs(time.time() - self.start_time)  # вычисляем прошедшее время
        r = 70  # радиус орбиты первой планеты
        planets_speed = [7, 4, 3, 1.6, 1.5, 1.2, 0.9, 0.8]
        planets_color = [
            (150, 160, 120),  # зеленый оттенок
            (255, 100, 0),  # Яркий оранжевый цвет
            (50, 205, 50),  # глубокий синий
            (220, 60, 30),  # Ярко-красный оттенок
            (255, 220, 90),  # Светло-желтый цвет
            (255, 130, 30),  # Оранжево-желтый цвет
            (0, 150, 200),  # Яркий голубой
            (20, 100, 230)  # Глубокий синий с фиолетовым оттенком
        ]
        def coord(center_x, center_y, radius1, radius2, speed=0, angele=0):
            angle_c = (elapsed_time * (sp_coeff + speed) * 360 / (2 * np.pi)) + angele  # вычисляем угол
            # для перемещения планеты по круговой траектории
            x = center_x + radius1 * np.cos(np.radians(angle_c))
            y = center_y + radius1 * np.sin(np.radians(angle_c))
            painter.drawEllipse(QPoint(int(x), int(y)), radius2, radius2)  # рисуем планету
            return int(x), int(y)

        for i, sp_coeff in enumerate(planets_speed):
            painter.setPen(QColor(*planets_color[i], 150))
            painter.setBrush(QColor(*planets_color[i], 150))
            crd = coord(400, 300, r, 20, angele=self.initial_angles[i])
            if i >= 2:
                # Рисуем спутник
                coord(crd[0], crd[1], 30, 3, speed=4)
                if i == 4:
                    coord(crd[0], crd[1], 30, 3, speed=3, angele=self.initial_angles[i])
                if i == 5:
                    #Кольца
                    painter.setBrush(QColor(*planets_color[i], 16))
                    painter.drawEllipse(QPoint(crd[0], crd[1]), 30, 30)
                    painter.drawEllipse(QPoint(crd[0], crd[1]), 35, 35)
                    painter.drawEllipse(QPoint(crd[0], crd[1]), 37, 37)
                    painter.drawEllipse(QPoint(crd[0], crd[1]), 40, 40)

            r += 20

app = QApplication(sys.argv)
window = Planets()
window.show()
sys.exit(app.exec())  # app.exec_() позволяет приложению получать события и обрабатывать их до тех пор,
# пока оно не будет закрыто