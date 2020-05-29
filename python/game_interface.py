from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from os.path import join
from PyQt5.QtCore import *
from settings import Settings
from style import Style
import time
from os.path import join

class GameInterface(Style):
    def __init__(self):
        super(GameInterface, self).__init__()
        self.setFixedSize(850, 700)
        self.setWindowIcon(QIcon(join(Settings.dir_logo, 'logo_1.png')))
        self.setWindowTitle("Space Invaders")
        self.setFocusPolicy(Qt.StrongFocus)
        self.game_interface()


    def game_interface(self):
        self.styles()
        self.draw_background()
        self.draw_additional_player()
        self.draw_score_text()

    def draw_score_text(self):
        """Отрисовка количества очков, набранных за одну игру"""

        self.score_label = QLabel("Score: 0", self)
        self.score_label.setStyleSheet(self.stylesheet)
        self.score_label.move(645, 643)
        self.score_label.resize(200, 40)

    def draw_additional_player(self):
        """Отрисовка допольнительных кораблей и линии, расположенной над ними"""

        self.line_label = QLabel(self)
        self.picture_line = QPixmap(
            join(Settings.dir_interface_graphics, "line.png")
        )
        self.line_label.setPixmap(self.picture_line)
        self.line_label.resize(820, 4)
        self.line_label.move(15, 630)

        self.line_label_2 = QLabel(self)
        self.picture_line_2 = QPixmap(join(Settings.dir_interface_graphics, "line_2.png"))
        self.line_label_2.setPixmap(self.picture_line_2)
        self.line_label_2.resize(820, 2)
        self.line_label_2.move(15, 558)

        self.dop_player_label_1 = QLabel(self)
        self.picture_dop_player = QPixmap(join(Settings.dir_player_graphics, "player_2.png"))
        self.dop_player_label_1.setPixmap(self.picture_dop_player)
        self.dop_player_label_1.resize(70, 40)
        self.dop_player_label_1.move(20, 645)

        self.dop_player_label_2 = QLabel(self)
        self.dop_player_label_2.setPixmap(self.picture_dop_player)
        self.dop_player_label_2.resize(70, 40)
        self.dop_player_label_2.move(95, 645)

    def redrawing_score(self):
        self.score_label.setText('Score: {}'.format(self.score))

    def redraw(self):
        self.line_label.resize(820, 2)
        self.line_label.move(15, 558)

    def redrawing_line(self):

        new_picture = QPixmap(join(Settings.dir_interface_graphics, "line_3.png"))
        for i in range(9):
            self.line_label_2.setPixmap(new_picture)
            QApplication.processEvents()
            time.sleep(0.1)
            self.line_label_2.setPixmap(self.picture_line_2)
            QApplication.processEvents()
            time.sleep(0.1)
