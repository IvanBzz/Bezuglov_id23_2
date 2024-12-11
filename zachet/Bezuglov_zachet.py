import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsEllipseItem, QSlider, QPushButton, QSpinBox, QVBoxLayout,
    QWidget
)
from PyQt6.QtCore import QTimer, Qt


class Particle(QGraphicsEllipseItem):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius, radius)
        self.setBrush(Qt.GlobalColor.white)
        self.dx = random.choice([-1, 1]) * random.uniform(1, 3)  # Увеличиваем скорость
        self.dy = random.choice([-1, 1]) * random.uniform(1, 3)  # Увеличиваем скорость

    def move(self):
        self.setPos(self.x() + self.dx, self.y() + self.dy)

        # Проверка на границы окна
        if self.x() <= 0 or self.x() >= 600 - self.rect().width():
            self.dx *= -1
        if self.y() <= 0 or self.y() >= 600 - self.rect().height():
            self.dy *= -1

    def check_collision(self, particles):
        for particle in particles:
            if particle != self:
                if self.collidesWithItem(particle):
                    # Отражение при столкновении
                    self.dx *= -1
                    self.dy *= -1


class ControlWidget(QWidget):
    def __init__(self, start_callback, reset_callback):
        super().__init__()

        # Элементы управления
        layout = QVBoxLayout(self)

        # Слайдер для количества частиц
        self.particle_count_slider = QSlider(Qt.Orientation.Horizontal)
        self.particle_count_slider.setRange(1, 100)
        self.particle_count_slider.setValue(20)
        layout.addWidget(self.particle_count_slider)

        # Слайдер для скорости частиц
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(20)
        layout.addWidget(self.speed_slider)

        # Спинбокс для радиуса частиц
        self.radius_spinbox = QSpinBox()
        self.radius_spinbox.setRange(15, 50)
        self.radius_spinbox.setValue(10)
        layout.addWidget(self.radius_spinbox)

        # Кнопка для запуска анимации
        self.start_button = QPushButton("Запустить анимацию")
        self.start_button.clicked.connect(start_callback)  # Привязка сигнала к функции запуска
        layout.addWidget(self.start_button)

        # Кнопка для сброса состояния
        reset_button = QPushButton("Сбросить частицы")
        reset_button.clicked.connect(reset_callback)  # Привязка сигнала к функции сброса
        layout.addWidget(reset_button)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анимация частиц")
        self.setGeometry(100, 100, 600, 600)

        # Создание сцены и представления
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        
        # Создание виджета управления и установка его как центрального
        self.control_widget = ControlWidget(self.start_animation, self.reset_particles)

        central_widget = QWidget()
        
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        
        central_widget.setLayout(layout)
        
        # Установка центрального виджета
        layout.addWidget(self.control_widget) 
        layout.addStretch()  
        
        self.setCentralWidget(central_widget)

        # Переменные для частиц и таймера
        self.particles = []
        
    def start_animation(self):
       # Удаляем старые частицы перед созданием новых
       self.reset_particles()

       count = self.control_widget.particle_count_slider.value()
       radius = self.control_widget.radius_spinbox.value()

       for _ in range(count):
           particle = Particle(random.randint(0, 590 - radius), random.randint(0, 590 - radius), radius)
           self.scene.addItem(particle)
           self.particles.append(particle)

       # Запуск таймера для обновления движения частиц
       speed = max(10, 100 - self.control_widget.speed_slider.value())  # Минимальная скорость таймера

       if hasattr(self, 'timer'):
           if self.timer.isActive():
               self.timer.stop()  # Остановить предыдущий таймер если он был запущен

       self.timer = QTimer()
       self.timer.timeout.connect(self.update_particles)
       self.timer.start(30)

    def reset_particles(self):
       for particle in self.particles:
           self.scene.removeItem(particle)

       self.particles.clear()

    def update_particles(self):
       for particle in self.particles:
           particle.move()
           particle.check_collision(self.particles)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
