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
        self.init_values()
        self.init_interface()

    def init_values(self):
        self.style = Style()
        self.x = self.style.x
        self.y = self.style.y

        self.time_enemies = None
        self.enemies = None

    def init_interface(self):
        self.buttons()
        self.labels()

    def labels(self):
        self.score_label = QLabel('Difficulty level ', self)
        self.score_label.setStyleSheet(self.style.stylesheet_score)
        self.score_label.move(self.x - self.x / 1.7, self.y - self.y / 1.9)
        self.score_label.resize(500, 60)

    def buttons(self):
        self.button_0 = QPushButton('For child', self)
        self.button_0.setStyleSheet(self.style.stylesheet_addit)
        self.button_0.clicked.connect(self.start_child)
        self.button_0.move(self.x - self.x / 1.4, self.y - self.y/8.5)
        self.button_0.setFixedSize(500, 50)


        self.button_1 = QPushButton('Easy', self)
        self.button_1.setStyleSheet(self.style.stylesheet_addit)
        self.button_1.clicked.connect(self.start_easy)
        self.button_1.move(self.x - self.x / 1.4, self.y + self.y / 8)
        self.button_1.setFixedSize(500, 50)

        self.button_2 = QPushButton('Normal', self)
        self.button_2.setStyleSheet(self.style.stylesheet_addit)
        self.button_2.clicked.connect(self.start_normal)

        self.button_2.move(self.x - self.x / 1.4, self.y + self.y/2.7)
        self.button_2.setFixedSize(500, 50)

        self.button_3 = QPushButton('No chance', self)
        self.button_3.setStyleSheet(self.style.stylesheet_addit)
        self.button_3.clicked.connect(self.start_no_chance)

        self.button_3.move(self.x - self.x / 1.4, self.y + self.y/1.62)
        self.button_3.setFixedSize(500, 50)

    def start_child(self):
        self.time_enemies = 0.8
        self.enemies = 10
        self.start_game()

    def start_easy(self):
        self.time_enemies = 0.8
        self.enemies = 20
        self.start_game()

    def start_normal(self):
        self.time_enemies = 0.8
        self.enemies = 40
        self.start_game()

    def start_no_chance(self):
        self.time_enemies = 0.09
        self.enemies = 40
        self.start_game()

    def start_game(self):
        self.close()
        window = GameEvents(Game(self.enemies, self.time_enemies))
        window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartInteraface()
    window.show()
    app.exec_()
