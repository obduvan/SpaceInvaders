from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
from signals import Signals
from settings import Settings
import random
from os import path


class Enemies:
    """Собственно космические захватчики"""

    def __init__(self, game_events_window):
        self.active_enemy = []
        self.game_events = game_events_window

        self.init_details()
        self.start_threads()

    def init_details(self):
        self.init_enemies()
        self.init_random_enemies()
        self.init_bullets()

    def start_threads(self):
        """Запуск всех потоков"""

        self.signal = Signals()
        self.start_random_enemy_thread()
        self.start_thread_enemies()
        self.start_thread_bullets()

    def init_bullets(self):
        """Инициализация, начальная отрисовка пуль захватчиков"""

        self.stack_bullets = []
        for i in range(4):
            self.stack_bullets.append(QLabel(self.game_events))
            self.stack_bullets[i].setPixmap(
                QPixmap(
                    path.join(
                        Settings.dir_bullets_graphics, "bullet_bad_{0}.png"
                    ).format(i % 2 + 3)
                )
            )
            self.stack_bullets[i].resize(5, 22)
            self.stack_bullets[i].move(0, 0)
            self.stack_bullets[i].hide()

    def start_thread_bullets(self):
        """Создание потоков для пуль"""

        self.signal.enemy_bullet_signal.connect(self.motion_bullets)
        self.thread_list_bullets = []
        for i in range(4):
            self.thread_list_bullets.append(
                MotionBullets(
                    self, self.matrix_enemies, self.signal, self.stack_bullets[i]
                )
            )
            self.thread_list_bullets[i].start()

    def start_random_enemy_thread(self):
        """Запуск летающего сверху корабля"""

        self.signal.enemy_random_signal.connect(self.motion_random_enemy)
        self.thread_dop_enemy = MotionDopThread(self.dop_enemy_label, self.signal)
        self.thread_dop_enemy.start()

    def motion_random_enemy(self, x, y):
        """Отрисовка летающего сверху корабля"""

        self.dop_enemy_label.move(self.dop_enemy_label.x() + x, y)

    def motion_bullets(self, bullet, x, y):
        """Отрисовка пуль захватчиков"""

        bullet.move(x, y)
        bullet.show()

    def start_thread_enemies(self):
        """Запуск потока для движение захватчиков"""

        self.signal.enemies_signal.connect(self.motion_enemies)
        self.thred = MotionThread(self, self.signal)
        self.thred.start()

    def init_random_enemies(self):
        """Cоздание летающего сверху корабля"""

        self.picture_dop_enemy = QPixmap(
            path.join(Settings.dir_enemies_graphics, "enem_dop_1.png")
        )
        self.dop_enemy_label = QLabel(self.game_events)
        self.dop_enemy_label.setPixmap(self.picture_dop_enemy)
        self.dop_enemy_label.resize(52, 30)
        self.dop_enemy_label.move(-60, 30)

    def motion_enemies(self, split_x, split_y, ind, i):
        """Отрисока двигающихся захватчиков"""

        enem = self.matrix_enemies[ind % 4][i % 10]
        self.matrix_enemies[ind % 4][i % 10].move(
            enem.x() + split_x, enem.y() + split_y
        )

    def init_enemies(self):
        """Создание захватчиков"""

        self.picture_enemy = QPixmap(
            path.join(Settings.dir_enemies_graphics, "enem_3.png")
        )
        self.matrix_enemies = [[] for i in range(4)]
        x, y = 20, 100
        ind = 0
        for i in range(40):
            if i % 10 == 0 and i != 0:
                ind += 1
                x = 20
                y += 50
            self.matrix_enemies[ind].append(QLabel(self.game_events))
            self.matrix_enemies[ind][i % 10].setPixmap(self.picture_enemy)
            self.matrix_enemies[ind][i % 10].resize(46, 38)
            self.matrix_enemies[ind][i % 10].move(x, y)
            x += 80


class MotionThread(QThread):
    """Поток для движения захватчков"""

    def __init__(self, enemies, signal):
        self.enemies = enemies
        self.signal = signal
        super(MotionThread, self).__init__()

    def run(self):
        """Цикл, управляющий движением захватчиков"""

        ind, i, straight, split_y = 0, 0, 0, 0
        split_x = 10

        while True:
            if i != 0:
                if i % 10 == 0:
                    ind += 1
                    straight += 1 / 16
                if i % 40 == 0:
                    time.sleep(70 / i + 0.8)
            if straight == 1:
                straight = 0
                split_y += 0.7
                split_x *= -1
            self.signal.enemies_signal.emit(split_x, split_y, ind, i)
            i += 1


class MotionDopThread(QThread):
    """Поток для движения сверху летающего корабля"""

    def __init__(self, enemy, signal):
        self.enemy = enemy
        self.signal = signal
        super(MotionDopThread, self).__init__()

    def run(self):
        """Цикл, управляющий движением сверху летающего корабля"""

        while True:
            random_time = random.randrange(13, 20)
            random_y = random.randrange(25, 32)
            time.sleep(random_time)
            while self.enemy.x() < 850:
                time.sleep(0.01)
                self.signal.enemy_random_signal.emit(1, random_y)
            self.signal.enemy_random_signal.emit(-910, random_y)


class MotionBullets(QThread):
    """Поток для пуль захватчиков"""

    def __init__(self, window, enemy, signal, bullet):
        self.matrix_enemy = enemy
        self.window = window
        self.bullet = bullet
        self.signal = signal
        super(MotionBullets, self).__init__()

    def registr_bullets(self, y):
        return y <= 710

    def run(self):
        """Цикл, управляющий полетом пуль захватчиков"""

        time.sleep(random.randrange(3, 13))

        while True:
            ind_1 = random.randrange(0, 3)
            ind_2 = random.randrange(0, 9)

            x = self.matrix_enemy[ind_1][ind_2].x() + 27
            y = self.matrix_enemy[ind_1][ind_2].y() + 30

            self.bullet.move(x, y)

            while self.registr_bullets(y):
                y += 1.5
                self.signal.enemy_bullet_signal.emit(self.bullet, x, y)
                time.sleep(0.01)

            self.bullet.move(ind_1, ind_2)
            self.bullet.hide()
