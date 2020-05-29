
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from signals import Signals
import time
from os import path
from settings import Settings
from radio import MusicBackground, MusicWin, MusicShoot

class Player:
    """Движение и выстрелы игрока"""

    def __init__(self, game_events_window):
        self.bullet_flag = True
        self.game_events = game_events_window

        self.signal = Signals()
        self.draw_player()
        self.init_bullet()
        self.init_bullets_thread()
        self.init_thread_on_shoot()

    def init_thread_on_shoot(self):
        self.signal.jesus.connect(self.jesus)
        self.signal.player_on_shoot_draw.connect(self.draw_on_shoot)
        self.signal.player_on_shoot_died.connect(self.player_died)
        self.thread_on_shoot = DrawOnShot(self.player_label, self.picture_player, self.signal, self)

    def jesus(self):
        self.player_label.setPixmap(self.picture_player)
        self.player_label.move(400, 560)
        self.player_label.show()

    def draw_on_shoot(self, picture):
        self.player_label.setPixmap(picture)

    def player_died(self):
        self.player_label.hide()

    def died_thread(self):
        self.thread_on_shoot.start()


    def draw_player(self):
        """Инициализация, отрисовка корабля игрока"""

        self.player_label = QLabel(self.game_events)
        self.picture_player = QPixmap(
            path.join(Settings.dir_player_graphics, "player_1.png")
        )
        self.player_label.setPixmap(self.picture_player)

        self.player_label.resize(70, 70)
        self.player_label.move(400, 560)

    def render_motion_bullet(self, bullet, x, y):
        """Отрисовка полета пуль игрока"""
        bullet.move(x, y)
        bullet.show()

    def init_bullets_thread(self):
        self.stack_thread = []
        self.signal.bullet_state_shoot.connect(self.reverse_bullet)
        self.signal.bullet_position_reverse.connect(self.start_position_bullet)
        self.signal.bullet_signal.connect(self.render_motion_bullet)
        self.bullet_thread = BulletPlayerThread(self.bullet_label, self.player_label, self.signal)

    def reverse_bullet(self, state):
        self.bullet_thread.stop = state

    def start_position_bullet(self, x, y):
        self.bullet_label.move(x, y)
        self.bullet_label.hide()

    def init_bullet(self):
        """Инициализация, начальная отрисовка пуль игрока"""

        self.bullet_label = QLabel(self.game_events)
        self.bullet_picture = QPixmap(path.join(Settings.dir_bullets_graphics, "bullet_3.png"))
        self.bullet_label.resize(5, 22)
        self.bullet_label.setPixmap(self.bullet_picture)

        self.bullet_label.hide()

    def motion_player(self, direction):
        """Выбор напраления движения игрока в зависимости от нажатой кнопки"""

        if direction == "left":
            if self.game_events.check_borders("left"):
                self.player_label.move(self.player_label.x() - 5, self.player_label.y())
        else:
            if self.game_events.check_borders("right"):
                self.player_label.move(self.player_label.x() + 5, self.player_label.y())


class BulletPlayerThread(QThread):
    """Поток для пуль игрока"""

    def __init__(self, bullet, player_label, signal):
        self.bullet = bullet
        self.player = player_label
        self.signal = signal
        self.stop = True
        self.music_shoot = MusicShoot()

        super(BulletPlayerThread, self).__init__()

    def check_wall(self, y):
        return y > -30 and self.stop

    def init_bullet(self):
        """Начальные координаты пуль, на основе координат игрока"""
        self.x = self.player.x() + 33
        self.y = self.player.y()

    def run(self):
        """Цикл полета пуль игрока"""
        self.init_bullet()
        # self.music_shoot.start()
        while self.check_wall(self.y):
            self.y -= 1
            time.sleep(0.001)
            self.signal.bullet_signal.emit(self.bullet, self.x, self.y)
        self.signal.bullet_position_reverse.emit(self.player.x(), self.player.y())


class DrawOnShot(QThread):
    """Изменение цвета при выстрела"""

    def __init__(self, player_label, norm_picture, signal, player_class):
        self.player_label = player_label
        self.norm_picture = norm_picture
        self.player_class = player_class
        self.signal = signal
        super(DrawOnShot, self).__init__()

    def run(self):
        self.died_label = QPixmap(
            path.join(Settings.dir_player_graphics, "Died_player.png")
        )
        self.died_label_1 = QPixmap(
            path.join(Settings.dir_player_graphics, "player_died_3.png")
        )
        self.player_class.bullet_flag = False
        self.signal.player_on_shoot_draw.emit(self.died_label)
        time.sleep(0.2)
        self.signal.player_on_shoot_died.emit()
        time.sleep(0.1)
        self.signal.jesus.emit()
        self.player_class.bullet_flag = True
