from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from os import path
from settings import Settings


class GameInterface(QMainWindow):
    """Отрисовка игрового интерфейса"""

    def __init__(self):
        super(GameInterface, self).__init__()
        self.setFixedSize(850, 700)
        self.setWindowTitle("Space Invaders")

        self.game_interface()

    def game_interface(self):
        self.styles()
        self.draw_background()
        self.draw_additional_player()
        self.draw_score_text()
        self.center()

    def styles(self):
        """Стили программы"""

        self.stylesheet = """
            QLabel{
                font: Lucida Console;
                color: #B200FF;
                font-size: 30px;
            }
            """

    def draw_background(self):
        """Отрисовка заднего фона"""

        self.setStyleSheet("background-color:  #0E0E0E")

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
            path.join(Settings.dir_interface_graphics, "line.png")
        )
        self.line_label.setPixmap(self.picture_line)
        self.line_label.resize(820, 4)
        self.line_label.move(15, 630)

        self.dop_player_label_1 = QLabel(self)
        self.picture_dop_player = QPixmap(
            path.join(Settings.dir_player_graphics, "player_2.png")
        )
        self.dop_player_label_1.setPixmap(self.picture_dop_player)
        self.dop_player_label_1.resize(70, 40)
        self.dop_player_label_1.move(20, 645)

        self.dop_player_label_2 = QLabel(self)
        self.dop_player_label_2.setPixmap(self.picture_dop_player)
        self.dop_player_label_2.resize(70, 40)
        self.dop_player_label_2.move(95, 645)

    def center(self):
        """Центрирование экрана"""

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2
        )
