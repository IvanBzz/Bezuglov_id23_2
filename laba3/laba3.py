from PyQt6.QtCore import QTimer, QPoint,Qt
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QColorDialog
import sys
import time
import json
import numpy as np


class Units:
    def __init__(self): #загрузка данных
        with open('planeti.json', 'r') as file:
            self.data = json.load(file)


class Customize_asteroid_window(QDialog): # диалоговое окно для задания параметров и создания астероида
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Настройка астероида")
        self.setGeometry(300, 200, 250, 150)
 
        self.ast_color = QColor(220, 220, 220) 
        # кнопка цвета
        self.colour_button = QPushButton("Choose Color", self)
        self.colour_button.setGeometry(10, 10, 100, 20)
        self.colour_button.clicked.connect(self.choose_color)

        self.radius_label = QLabel("Radius:", self)
        self.radius_label.setGeometry(10, 40, 50, 20)

        # слайдер для задания размера
        self.radius_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.radius_slider.setGeometry(70, 40, 150, 20)
        # ограниечения значений размера:
        self.radius_slider.setMinimum(3)
        self.radius_slider.setMaximum(40)
        self.radius_slider.setValue(10) 

        self.direction_label = QLabel("Degrees:", self)
        self.direction_label.setGeometry(10, 80, 50, 20)

        # слайдер для задания направления
        self.direction_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.direction_slider.setGeometry(70, 80, 150, 20)
        # ограниечения значений направления:
        self.direction_slider.setMinimum(-360)
        self.direction_slider.setMaximum(360)
        self.direction_slider.setValue(90) 

        self.speed_slider = QLabel("Speed:", self)
        self.speed_slider.setGeometry(10, 60, 50, 20) 

        # слайдер для скорости
        self.speed_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.speed_slider.setGeometry(70, 60, 150, 20)
        # ограниечения значений скорости:
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(5)
        self.speed_slider.setValue(3)
        '''кнопка отмены'''
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setGeometry(150, 110, 50, 20)
        self.cancel_button.clicked.connect(self.reject)
        '''подтверждение'''
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setGeometry(80, 110, 50, 20)
        self.ok_button.clicked.connect(self.accept)

    def choose_color(self): 
        color = QColorDialog.getColor(QColor(0, 0, 255), self)
        if color.isValid():
            self.ast_color = color

    def get_ast_parameters(self): 
        return self.ast_color, int(self.radius_slider.value()),int(self.direction_slider.value()), int(self.speed_slider.value())

class Low_cel_body:
    def __init__(self,color, position, radius, degrees, skorost):
        self.degrees = degrees  
        self.skorost = skorost
        self.loct = position
        self.color=color
        self.x_crd = int(self.loct.x())
        self.y_crd = int(self.loct.y())
        self.radius = radius
        

    def locations_aster(self):
        dx = np.cos(np.radians(self.degrees)) * self.skorost 
        dy = np.sin(np.radians(self.degrees))* self.skorost
        self.x_crd = self.x_crd+ int(dx)
        self.y_crd = self.y_crd+ int(dy)
        self.loct = QPoint(self.x_crd, self.y_crd)

class Solar_systemm(QWidget):
    def __init__(self):
        super().__init__()
        self.st = time.time()
        self.status_pause=False
        self.a=list()
        self.when_paused = 0  
        self.paused_time = 0 
        self.total_time = 0

        self.setWindowTitle("Bezuglov laba 3")
        self.setGeometry(200, 100, 1000, 1000)
        self.center_x = 500
        self.center_y = 500
        
        self.pixmap = QPixmap('i.png')   

        self.schetchik = QTimer()
        self.schetchik.timeout.connect(self.update)
        self.schetchik.start(10)
    
        self.knopka_P = QPushButton('Pause', self)
        self.knopka_P.setGeometry(10, 10, 100, 50)
        self.knopka_P.clicked.connect(self.stopped)

        self.data_p=Units().data

    def stolk(self, crd, planet, cel_b, asteroid_number):
        return (abs(crd[asteroid_number][0]-cel_b.x_crd) < planet['radius']+ cel_b.radius ) and (abs(crd[asteroid_number][1]-cel_b.y_crd) < planet['radius']+ cel_b.radius)
        

    def stopped(self):
        self.status_pause = not self.status_pause  
        if self.status_pause:
            self.knopka_P.setText("Continue")  
            self.when_paused = time.time() 
        else:
            self.knopka_P.setText("Stop")  
            self.paused_time += time.time() - self.when_paused 

    def paintEvent(self, event):
        
        rds = 0
        crd=[]
        pnt_tool = QPainter(self)
        pnt_tool.drawPixmap(self.rect(), self.pixmap)
        if not self.status_pause:
            self.total_time = abs(self.st-time.time()) - self.paused_time
        
        def location(center_x, center_y, orbit, razmer, skorost, ugl=0):
            ugol = ugl + self.total_time*skorost*360/(2*np.pi)
            x = int(orbit * np.cos(np.radians(ugol))+center_x)
            y = int(orbit * np.sin(np.radians(ugol))+center_y)
            pnt_tool.drawEllipse(QPoint(int(x), int(y)), razmer, razmer)  #отрисовываем планеты
            return int(x),int(y)

        
        for planet_number in range(len(self.data_p)):
            k=self.data_p[planet_number]
            pnt_tool.setPen(QColor(*k['color']))
            pnt_tool.setBrush(QColor(*k['color']))

            if planet_number==0:
                #SUN
                pnt_tool.setPen(QColor(255, 255, 0))
                pnt_tool.setBrush(QColor(255, 255, 0))
                pnt_tool.drawEllipse(QPoint(500, 500), 60, 60)
                crd.append(location(500,500,rds,k['radius'],k['skorost'],k['initial_angle']))
                continue

            rds += self.data_p[planet_number-1]['radius'] + 5 + k['radius']
            
            loc = location(500, 500, rds, k['radius'],
                                k['skorost'],
                                  k['initial_angle'])
            crd.append(loc)

            if planet_number==6:
                for i in range(4):
                    pnt_tool.setBrush(QColor(*k['color'], 16))
                    pnt_tool.drawEllipse(QPoint(loc[0], loc[1]), k['radius'] + 10+i*3,
                                        k['radius'] + 10+i*3)

            if 'sputnik' in k.keys():
                for sputnik in k['sputnik']:
                    pnt_tool.setPen(QColor(*sputnik['color']))
                    pnt_tool.setBrush(QColor(*sputnik['color']))
                    location(loc[0], loc[1], k['radius']+7, sputnik['radius'],
                                sputnik['skorost'], sputnik['initial_angle'])
            else: 
                None

            
                
        for cel_b in self.a:

            for asteroid_number in range(len(self.data_p)):
                j=self.data_p[asteroid_number]
                if self.stolk(crd, j, cel_b, asteroid_number)==False:
                    pnt_tool.setBrush(QColor(255, 255, 255))
                    pnt_tool.drawEllipse(cel_b.loct.x() - cel_b.radius,
                                        cel_b.loct.y() - cel_b.radius,
                                        cel_b.radius,
                                        cel_b.radius)
                else:
                    self.data_p[asteroid_number]['radius'] = cel_b.radius // 2 +j['radius']
                    self.a.remove(cel_b)  
            '''Обновляем локацию астероида'''
            if not self.status_pause:
                cel_b.locations_aster()   

    def mousePressEvent(self, event): 
        if event.button() == Qt.MouseButton.LeftButton:
            dialog = Customize_asteroid_window(self)
            if self.exec_settings_dialog(dialog) == 1:# если кликнули - всплывает окно
                self.body_position = QPoint(event.pos().x(), event.pos().y()) # получем значения из диалогового окна
                color, radius,degrees, skorost = dialog.get_ast_parameters()
                ast = Low_cel_body(color, self.body_position, radius, degrees,skorost)
                self.a.append(ast)
    def exec_settings_dialog(self, dialog): # создание и запуск диалогового окна
        return dialog.exec() 




    

    
    

    
kosmos = QApplication(sys.argv)
wnww = Solar_systemm()
wnww.show()
sys.exit(kosmos.exec())  
