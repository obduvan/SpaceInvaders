from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from signals import Signals
import time
from os import path
from settings import Settings


class Player:
    """Движение и выстрелы игрока"""

    def __init__(self, game_events_window):
        self.game_events = game_events_window

        self.signal = Signals()
        self.draw_player()
        self.init_bullet()
        self.init_bullets_thread()

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
        self.signal.bullet_signal.connect(self.render_motion_bullet)
        self.stack_thread.append(
            BulletPlayerThread(self.bullet_label, self.player_label, self.signal)
        )
        self.stack_thread.append(
            BulletPlayerThread(self.bullet_label_2, self.player_label, self.signal)
        )

    def init_bullet(self):
        """Инициализация, начальная отрисовка пуль игрока"""

        self.bullet_label, self.bullet_label_2 = (
            QLabel(self.game_events),
            QLabel(self.game_events),
        )
        self.bullet_picture = QPixmap(
            path.join(Settings.dir_bullets_graphics, "bullet_3.png")
        )
        self.bullet_label.resize(4, 22)
        self.bullet_label.setPixmap(self.bullet_picture)
        self.bullet_label_2.resize(4, 22)
        self.bullet_label_2.setPixmap(self.bullet_picture)
        self.bullet_label_2.hide(), self.bullet_label.hide()

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

    def __init__(self, bullet, player, signal):
        self.bullet = bullet
        self.player = player
        self.signal = signal
        super(BulletPlayerThread, self).__init__()

    def check_rules_button(self):
        """Проверка на касание (добавлю позже), выход за рамки карты"""

        return self.bullet.y() > -14

    def init_bullet(self):
        """Начальные координаты пуль, на основе координат игрока"""

        self.x = self.player.x() + 33
        self.y = self.player.y()

    def run(self):
        """Цикл полета пуль игрока"""

        self.init_bullet()

        while True:
            self.y -= 1
            time.sleep(0.001)
            self.signal.bullet_signal.emit(self.bullet, self.x, self.y)
