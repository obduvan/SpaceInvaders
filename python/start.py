import sys
from os.path import join

from PyQt5.QtWidgets import QPushButton, QApplication, QLabel
from settings import Settings, Game
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from style import Style
from game_events import GameEvents


class StartInteraface(Style):
    def __init__(self):
        super(StartInteraface, self).__init__()
        self.setFixedSize(850, 700)

        self.setWindowIcon(QIcon(join(Settings.dir_logo, 'logo_1.png')))
        self.setWindowTitle("Space Invaders")
        self.setFocusPolicy(Qt.StrongFocus)
        self.init_interface()

    def init_interface(self):
        self.buttons()
        self.labels()

    def labels(self):
        self.score_label = QLabel('Select difficulty', self)
        self.score_label.setStyleSheet(self.stylesheet_score)
        self.score_label.move(250, 140)
        self.score_label.resize(500, 60)

    def buttons(self):
        self.button_0 = QPushButton('For child', self)
        self.button_0.setStyleSheet(self.stylesheet_addit)
        self.button_0.clicked.connect(self.start_child)
        self.button_0.move(180, 265)
        self.button_0.setFixedSize(500, 50)


        self.button_1 = QPushButton('Easy', self)
        self.button_1.setStyleSheet(self.stylesheet_addit)
        self.button_1.clicked.connect(self.start_easy)
        self.button_1.move(180, 335)
        self.button_1.setFixedSize(500, 50)

        self.button_2 = QPushButton('Normal', self)
        self.button_2.setStyleSheet(self.stylesheet_addit)
        self.button_2.clicked.connect(self.start_normal)

        self.button_2.move(180, 405)
        self.button_2.setFixedSize(500, 50)

        self.button_3 = QPushButton('No chance', self)
        self.button_3.setStyleSheet(self.stylesheet_addit)
        self.button_3.clicked.connect(self.start_no_chance)

        self.button_3.move(180, 475)
        self.button_3.setFixedSize(500, 50)

    def start_child(self):
        self.time_enemies = 0.8
        self.enemies = 10
        self.step_time = 20
        self.limit_step = 0.5
        self.start_game()

    def start_easy(self):
        self.time_enemies = 0.8
        self.enemies = 20
        self.step_time = 40
        self.limit_step = 1
        self.start_game()

    def start_normal(self):
        self.time_enemies = 0.8
        self.enemies = 40
        self.step_time = 40
        self.limit_step = 1
        self.start_game()

    def start_no_chance(self):
        self.time_enemies = 0.08
        self.enemies = 40
        self.step_time = 40
        self.limit_step = 1
        self.start_game()

    def start_game(self):
        self.close()
        window = GameEvents(Game(self.enemies, self.time_enemies,  self.step_time, self.limit_step))
        window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartInteraface()
    window.show()
    app.exec_()
