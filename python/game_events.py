import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
from game_interface import GameInterface
from enemies import Enemies
from player import Player, BulletPlayerThread
from signals import Signals
import subprocess
from questions import QuestionsInterface
from os import path

from settings import Settings


class GameEvents(GameInterface):
    """
    Считывание, проверка событий во время игровой сессии и запуск персонажей
    Здесь еще частичное управление главного игрока,  в будушем уберу отсюда.
    """

    def __init__(self, game_settings):
        super(GameEvents, self).__init__()
        self.kill = 0
        self.game_settings = game_settings
        self.set_frequency_render()
        self.render_details()

    def set_frequency_render(self):
        self.timer = QBasicTimer()
        self.timer.start(10, self)

    def init_player(self):
        self.stop_game = False
        self.player = Player(self)
        self.old_bullet_enem = None
        self.old_bullet_pl = None
        self.score = 0

    def init_enemies(self):
        self.enemies = Enemies(self, self.signal, self.game_settings)

    def init_signals(self):
        self.signal = Signals()

        self.signal.closed_signal.connect(self.close_game)
        self.signal.stop_game_singal.connect(self.menu)
        self.signal.restart_signal.connect(self.restart_game)
        self.signal.reverse_bullet_player.connect(self.player.reverse_bullet)

    def render_details(self):
        self.init_player()
        self.init_signals()
        self.init_enemies()
        self.init_values()

    def init_values(self):
        self.boomm, self.traffic_left, self.traffic_right = False, False, False

    def check_borders(self, direction):
        x = self.player.player_label.x()
        if direction == "left":
            return x > 0
        else:
            return x < 780

    def keyPressEvent(self, QKeyEvent):
        """
        Фиксирование нажатых кнопокж.
        Запуск потока пуль иг   рока.
        """
        if not self.stop_game:
            even_key = QKeyEvent.key()
            if even_key == Qt.Key_Right:
                self.traffic_right = True
            if even_key == Qt.Key_Left:
                self.traffic_left = True
            if even_key == Qt.Key_Space:
                if self.player.bullet_flag:
                    self.signal.reverse_bullet_player.emit(True)
                    self.player.bullet_thread.start()

    def keyReleaseEvent(self, event):
        """Фиксирование отжатых кнопок, во благо плавности"""

        key = event.key()

        if key == Qt.Key_Right and not event.isAutoRepeat() and self.traffic_right:
            self.traffic_right = False
        if key == Qt.Key_Left and not event.isAutoRepeat() and self.traffic_left:
            self.traffic_left = False

    def hide_dop_player(self, check):
        if check % 2 == 0:
            self.dop_player_label_2.hide()
        else:
            self.dop_player_label_1.hide()

    def timerEvent(self, event):
        """Движение главного игрока
         Проверка выстрелов в игрока"""

        if not self.stop_game:
            if self.traffic_left:
                self.player.motion_player("left")
            if self.traffic_right:
                self.player.motion_player("right")

        bullet_en = self.enemies.registr_bullet_hit_en(self.player)
        self.game_event(bullet_en)

    def game_event(self, bullet_en):
        if bullet_en != self.old_bullet_enem and bullet_en and self.kill < 3:
            self.old_bullet_enem = bullet_en
            self.player.died_thread()
            self.traffic_right, self.traffic_left = False, False
            self.hide_dop_player(self.kill)
            self.kill += 1

        if self.kill == 2:
            self.kill += 1
            self.menu(False, False)

        answer, killed_enemies = self.enemies.registr_bullet_hit_pl(self.player)
        if answer > 0:
            self.signal.reverse_bullet_player.emit(False)
            self.score += answer
            self.redrawing_score()

        if killed_enemies:
            self.menu(False, True)

    def menu(self, draw_line, result_game):
        if not self.stop_game:
            self.enemies.kill_threads()
            self.stop_game = True
            if draw_line:
                self.redrawind_line()

            self.enemies.signal.hide_enemies_signal.emit()
            self.draw_menu(result_game)

    def draw_menu(self, result_game):
        # time.sleep(1)
        new_win = QuestionsInterface(self, self.signal, self.score, result_game)
        new_win.show()

    def redrawing_score(self):
        self.score_label.setText('Score: {}'.format(self.score))

    def redraw(self):
        self.line_label.resize(820, 2)
        self.line_label.move(15, 558)

    def redrawind_line(self):
        new_piscture = QPixmap(
            path.join(Settings.dir_interface_graphics, "line_3.png"))
        for i in range(9):
            self.line_label_2.setPixmap(new_piscture)
            QApplication.processEvents()
            time.sleep(0.1)
            self.line_label_2.setPixmap(self.picture_line_2)
            QApplication.processEvents()
            time.sleep(0.1)

    def restart_game(self):
        self.close_game()
        subprocess.Popen("python " + "start.py", shell=True)

    def close_game(self):
        self.close()

    def closeEvent(self, event):
        self.close_game()


