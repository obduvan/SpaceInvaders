from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os.path import join
from settings import Settings
from signals import Signals
from time import sleep
from event_checker import ShotReg


class Defenders:
    def __init__(self, game_events, player, enemies):
        self.game_events = game_events
        self.player = player
        self.enemies = enemies
        self.draw_defenders()
        self.init_signal()
        self.init_thread()

    def init_signal(self):
        self.signal = Signals()
        self.signal.defender_player_signal.connect(self.player.reverse_bullet)
        self.signal.redraw_defender_signal.connect(self.redrawing_defender)
        self.signal.defender_enemy_signal.connect(self.enemies.hide_bullets)

    def init_thread(self):
        self.defender_thread = DefendersThread(self.killed_defenders_state, self.signal, self.matrix_defenders,
                                               self.player.bullet_label, self.enemies)
        self.defender_thread.start()

    def draw_defenders(self):
        self.killed_defenders_state = {}
        self.matrix_defenders = []
        coordinates = [(70, 470), (120, 430), (170, 430), (220, 470)]
        split_x = 0
        for x in range(3):
            for i in range(4):
                defender = QLabel(self.game_events)
                picture = QPixmap(join(Settings.dir_defenders, "def.png"))
                defender.setPixmap(picture)
                defender.resize(35, 35)
                defender.move(coordinates[i][0] + split_x, coordinates[i][1])
                self.killed_defenders_state.update({str(defender): ['None', 0]})
                self.matrix_defenders.append(defender)
            split_x += 250

    def redrawing_defender(self, defender, hide):
        if hide:
            defender.hide()
        else:
            picture = QPixmap(join(Settings.dir_defenders, "def_2.png"))
            defender.setPixmap(picture)
            defender.show()

    def kill_threads(self):
        self.defender_thread.terminate()


class DefendersThread(QThread):
    def __init__(self, killed_defenders_state, signal, matrix_defenders, player_bullet_label, enemies):
        self.matrix_defenders = matrix_defenders
        self.signal = signal
        self.killed_defenders_state = killed_defenders_state
        self.player_bullet_label = player_bullet_label
        self.count_defenders = 0
        self.enemies = enemies
        self.enemies_bullets = self.enemies.stack_bullets
        self.matrix_enemies = self.enemies.matrix_enemies
        super(DefendersThread, self).__init__()

    def checker(self, bullet, defender, who):
        count = self.killed_defenders_state.get(str(defender))[1]
        if count < 2:
            flag = False
            if who == 'player':
                self.signal.defender_player_signal.emit(False)
                self.killed_defenders_state.get(str(defender))[1] += 1
                self.killed_defenders_state.get(str(defender))[0] = 'player'
            elif who == 'enemies':
                last_bullet = self.killed_defenders_state.get(str(defender))[0]
                if last_bullet != str(bullet):
                    self.signal.defender_enemy_signal.emit(bullet)
                    self.killed_defenders_state.get(str(defender))[1] += 1
                    self.killed_defenders_state.get(str(defender))[0] = str(bullet)
            else:
                self.killed_defenders_state.get(str(defender))[1] += 228
            if self.killed_defenders_state.get(str(defender))[1] >= 2:
                flag = True
            self.signal.redraw_defender_signal.emit(defender, flag)

    def check_enemies(self, a, b, defender):
        for enemy_list in self.matrix_enemies:
            for enemy in enemy_list:
                a1 = (enemy.x(), enemy.y())
                b1 = (a1[0] + 46, a1[1] + 38)
                if str(enemy) not in self.enemies.died_enemies:
                    if ShotReg.shot_registration(a, b, a1, b1):
                        self.checker(enemy, defender, 'jesus')

    def run(self):
        while True:
            sleep(0.01)
            for defender in self.matrix_defenders:
                a = (defender.x(), defender.y())
                b = (a[0] + 35, a[1] + 35)
                for bullet_enemies in self.enemies_bullets:
                    a1 = (bullet_enemies.x(), bullet_enemies.y())
                    b1 = (a1[0] + 5, a1[1] + 22)
                    if ShotReg.shot_registration(a, b, a1, b1):
                        self.checker(bullet_enemies, defender, 'enemies')
                self.check_enemies(a, b, defender)

                a1 = (self.player_bullet_label.x(), self.player_bullet_label.y())
                b1 = (a1[0] + 5, a1[1] + 22)

                if ShotReg.shot_registration(a, b, a1, b1):
                    self.checker(self.player_bullet_label, defender, 'player')
