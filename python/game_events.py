import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from game_interface import GameInterface
from enemies import Enemies
from player import Player, BulletPlayerThread
from signals import Signals
from questions import QuestionsInterface

from radio import MusicBackground, MusicWin, MusicShoot, MusicKill, MusicShootEnem

from event_checker import EventChecker
from defenders import Defenders


class GameEvents(GameInterface, EventChecker):
    """
    Считывание, проверка событий во время игровой сессии и запуск персонажей
    Здесь еще частичное управление главного игрока,  в будушем уберу отсюда.
    """

    def __init__(self, game_settings):
        super(GameEvents, self).__init__()
        self.jesus = False
        self.flag = False
        self.game_settings = game_settings
        self.set_frequency_render()
        self.render_details()
        # self.init_music()

    def init_music(self):
        self.music_back = MusicBackground()
        self.music_back.start()

        self.music_kill = MusicKill()
        self.music_win = MusicWin()
        self.music_shoot = MusicShootEnem()

    def set_frequency_render(self):
        self.timer = QBasicTimer()
        self.timer.start(10, self)

    def init_player(self):
        self.stop_game = False
        self.player = Player(self)
        self.old_bullet_enem = None
        self.old_bullet_pl = None

    def init_enemies(self):
        self.enemies = Enemies(self, self.signal, self.game_settings)

    def init_signals(self):
        self.signal = Signals()
        self.signal.closed_signal.connect(self.close_game)
        self.signal.stop_game_singal.connect(self.menu)
        self.signal.restart_signal.connect(self.restart_game)
        self.signal.reverse_bullet_player.connect(self.player.reverse_bullet)

    def init_defenders(self):
        self.defenders = Defenders(self, self.player, self.enemies)

    def render_details(self):
        self.init_player()
        self.init_signals()
        self.init_enemies()
        self.init_values()
        self.init_defenders()

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
        if not self.stop_game and not self.flag:
            even_key = QKeyEvent.key()
            if even_key == Qt.Key_Right:
                self.traffic_right = True
            if even_key == Qt.Key_Left:
                self.traffic_left = True
            if even_key == Qt.Key_Space:
                self.jesus = False
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
        if bullet_en != self.old_bullet_enem and bullet_en and self.lives > 0 and not self.jesus:
            self.jesus = True
            self.old_bullet_enem = bullet_en

            self.player.died_thread()
            self.traffic_right, self.traffic_left = False, False
            self.hide_dop_player(self.lives)
            # self.music_kill.start()
            self.count_lives()

        if self.stop_game:
            self.menu(False, False)

        answer, killed_enemies = self.enemies.registr_bullet_hit_pl(self.player)
        if answer > 0:
            # self.music_shoot.start()
            self.signal.reverse_bullet_player.emit(False)

            self.count_score(answer)
            self.redrawing_score()

        if killed_enemies:
            self.menu(False, True)

    def kill_threads(self):
        self.defenders.kill_threads()
        self.enemies.kill_threads()

    def menu(self, draw_line, result_game):
        if not self.flag:
            self.flag = True
            self.kill_threads()
            if draw_line:
                # self.music_event()

                self.redrawing_line()
            self.enemies.signal.hide_enemies_signal.emit()
            self.draw_menu(result_game)

    def music_event(self):
        self.music_back.terminate()
        self.music_kill.start()

    def draw_menu(self, result_game):
        self.close()
        new_win = QuestionsInterface(self, self.signal, self.score, result_game)
        new_win.show()

    def restart_game(self):
        self.close_game()
        os.system("python start.py")

    def close_game(self):
        self.close()

    def closeEvent(self, event):
        self.close_game()
