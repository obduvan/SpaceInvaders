from PyQt5.QtCore import *
from PyQt5.QtGui import *
from game_interface import GameInterface
from enemies import Enemies
from player import Player, BulletPlayerThread


class GameEvents(GameInterface):
    """Считывание, проверка событий во время игровой сессии и запуск персонажей

        Здесь еще частичное управление главного игрока,  в будушем уберу отсюда.
    """

    def __init__(self):
        super(GameEvents, self).__init__()
        self.set_frequency_render()
        self.render_details()

    def set_frequency_render(self):
        self.timer = QBasicTimer()
        self.timer.start(10, self)

    def init_player(self):
        self.player = Player(self)

    def init_enemies(self):
        self.enemies = Enemies(self)

    def render_details(self):
        self.init_values()
        self.init_player()
        self.init_enemies()

    def init_values(self):
        self.boomm, self.traffic_left, self.traffic_right = False, False, False
        self.k = 0  # костыль для запуска конечного числа потоков для пуль

    def check_borders(self, direction):
        x = self.player.player_label.x()
        if direction == "left":
            return x > 0
        else:
            return x < 780

    def keyPressEvent(self, QKeyEvent):
        """Фиксирование нажатых кнопокж.

           Запуск потока пуль игрока.
        """

        even_key = QKeyEvent.key()
        if even_key == Qt.Key_Right:
            self.traffic_right = True
        if even_key == Qt.Key_Left:
            self.traffic_left = True
        if even_key == Qt.Key_Space:
            if self.k < 2:
                self.player.stack_thread[self.k % 2].start()
            else:
                self.player.stack_thread[self.k % 2].init_bullet()
            self.k += 1

    def keyReleaseEvent(self, event):
        """Фиксирование отжатых кнопок, во благо плавности"""

        key = event.key()
        if key == Qt.Key_Right and not event.isAutoRepeat() and self.traffic_right:
            self.traffic_right = False
        if key == Qt.Key_Left and not event.isAutoRepeat() and self.traffic_left:
            self.traffic_left = False

    def timerEvent(self, e):
        """Движение главного игрока"""

        if self.traffic_left:
            self.player.motion_player("left")
        if self.traffic_right:
            self.player.motion_player("right")
