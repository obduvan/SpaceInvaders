from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
from signals import Signals
from settings import Settings, Game
import random
from event_checker import ShotReg
from os import path


class Enemies:
    """Собственно космические захватчики"""

    def __init__(self, game_events_window, parent_signal, game_settings):
        self.parent_signal = parent_signal
        self.game_settings = game_settings
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

        self.bullets = 4
        self.signal.enemy_bullet_signal.connect(self.motion_bullets)
        self.thread_list_bullets = {}
        for i in range(self.bullets):
            self.thread_list_bullets.update({str(self.stack_bullets[i]):
                MotionBullets(
                    self, self.matrix_enemies, self.signal, self.stack_bullets[i], self.died_enemies, self.enemies_index
                )})
            self.thread_list_bullets[str(self.stack_bullets[i])].start()

    def start_random_enemy_thread(self):
        """Запуск летающего сверху корабля"""

        self.signal.enemy_random_signal.connect(self.motion_random_enemy)
        self.thread_dop_enemy = MotionDopThread(self.dop_enemy_label, self.signal)
        self.thread_dop_enemy.start()

    def motion_random_enemy(self, x, y, state):
        """Отрисовка летающего сверху корабля"""
        if state == 1:
            self.dop_enemy_label.show()

        self.dop_enemy_label.move(self.dop_enemy_label.x() + x, y)

    def enum_bullets(self, a, b):
        for bullet in self.stack_bullets:
            a1 = (bullet.x(), bullet.y())
            b1 = (a1[0] + 5, a1[1] + 22)
            if ShotReg.shot_registration(a, b, a1, b1):
                return bullet

    def registr_bullet_hit_en(self, target):
        a = (target.player_label.x() + 10, target.player_label.y() + 10)
        b = (a[0] + 60, a[1] + 60)
        return self.enum_bullets(a, b)

    def for_in_enemies(self, a1, b1):
        count_killed = 0
        killed = False
        for enemy_list in self.matrix_enemies:
            for enemy in enemy_list:
                a = (enemy.x(), enemy.y())
                b = (a[0] + 46, a[1] + 38)
                if str(enemy) not in self.died_enemies:
                    if ShotReg.shot_registration(a, b, a1, b1):
                        self.died_enemies.append(str(enemy))
                        enemy.hide()
                        count_killed += 1

        a = (self.dop_enemy_label.x(), self.dop_enemy_label.y())
        b = (a[0] + 46, a[1] + 38)
        if ShotReg.shot_registration(a, b, a1, b1):
            self.dop_enemy_label.hide()
            count_killed += 1
        if len(self.died_enemies) == self.game_settings.enemies:
            killed = True

        return count_killed, killed

    def registr_bullet_hit_pl(self, player):
        bullet_a = (player.bullet_label.x(), player.bullet_label.y())
        bullet_b = bullet_a[0] + 5, bullet_a[1] + 22
        return self.for_in_enemies(bullet_a, bullet_b)

    def motion_bullets(self, bullet, x, y):
        """Отрисовка пуль захватчиков"""

        bullet.move(x, y)
        bullet.show()

    def start_thread_enemies(self):
        """Запуск потока для движение захватчиков"""

        self.signal.hide_enemies_signal.connect(self.hide_enemies)
        self.signal.enemies_signal.connect(self.motion_enemies)
        self.thred = MotionThread(self, self.signal, self.game_settings)
        self.thred.start()

    def kill_threads(self):
        self.thread_dop_enemy.terminate()
        self.thred.terminate()
        for i in range(self.enemies_index):
            self.thread_list_bullets[str(self.stack_bullets[i])].terminate()

    def hide_enemies(self):
        ind = 0
        for i in range(self.game_settings.enemies):
            if i % 10 == 0 and i != 0:
                ind += 1
            self.matrix_enemies[ind][i % 10].hide()
        for i in range(self.enemies_index):
            self.stack_bullets[i].hide()

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

        enem = self.matrix_enemies[ind % self.enemies_index][i % 10]
        x = enem.x() + split_x
        y = enem.y() + split_y
        if str(enem) not in self.died_enemies:
            self.matrix_enemies[ind % self.enemies_index][i % 10].move(x, y)
            if 520 <= y < 800:
                self.parent_signal.stop_game_singal.emit(True, False)

    def init_enemies(self):
        """Создание захватчиков"""

        self.enemies_index = max(1, int(self.game_settings.enemies / 10))
        self.died_enemies = []
        self.picture_enemy = QPixmap(
            path.join(Settings.dir_enemies_graphics, "enem_3.png")
        )
        self.matrix_enemies = [[] for i in range(4)]
        x, y = 20, 100
        ind = 0
        for i in range(self.game_settings.enemies):
            if i % 10 == 0 and i != 0:
                ind += 1
                x = 20
                y += 50
            self.matrix_enemies[ind].append(QLabel(self.game_events))
            self.matrix_enemies[ind][i % 10].setPixmap(self.picture_enemy)
            self.matrix_enemies[ind][i % 10].resize(46, 38)
            self.matrix_enemies[ind][i % 10].move(x, y)

            x += 80

    def hide_bullets(self, bullet):
        self.thread_list_bullets[str(bullet)].terminate()
        bullet.hide()

        self.thread_list_bullets[str(bullet)].start()


class MotionThread(QThread):
    """Поток для движения захватчков"""

    def __init__(self, enemies, signal, game_settings):
        self.enemies = enemies
        self.game_settings = game_settings
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
                if i % self.game_settings.step_time == 0:
                    time.sleep(self.game_settings.time_enemies)
            if straight >= self.game_settings.limit_step:
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
            random_time = random.randrange(10, 15)
            random_y = random.randrange(25, 32)
            time.sleep(random_time)

            while self.enemy.x() < 850:
                time.sleep(0.01)
                self.signal.enemy_random_signal.emit(1, random_y, 2)
            self.signal.enemy_random_signal.emit(-910, random_y, 1)


class MotionBullets(QThread):
    """Поток для пуль захватчиков"""

    def __init__(self, window, enemy, signal, bullet, died_enemies, enemies_index):
        self.matrix_enemy = enemy
        self.enemies_index = enemies_index
        self.died_enemies = died_enemies
        self.window = window
        self.bullet = bullet
        self.signal = signal

        super(MotionBullets, self).__init__()

    def registr_bullets(self, y):
        return y <= 710

    def run(self):
        """Цикл, управляющий полетом пуль захватчиков"""
        time.sleep(random.randrange(3, 8))

        while True:
            ind_1 = random.randrange(0, max(self.enemies_index - 1, 1))
            ind_2 = random.randrange(0, 10)
            if str(self.matrix_enemy[ind_1][ind_2]) not in self.died_enemies:

                x = self.matrix_enemy[ind_1][ind_2].x() + 27
                y = self.matrix_enemy[ind_1][ind_2].y() + 30

                self.bullet.move(x, y)

                while self.registr_bullets(y):
                    y += 1.5
                    self.signal.enemy_bullet_signal.emit(self.bullet, x, y)
                    time.sleep(0.01)

                self.bullet.move(ind_1, ind_2)
                self.bullet.hide()
