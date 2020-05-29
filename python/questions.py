from PyQt5.QtWidgets import QLabel, QPushButton, QMainWindow
from style import Style
from settings import Settings
from radio import MusicWin, MusicLose

class QuestionsInterface(QMainWindow):
    def __init__(self, parent, signal, score, result_game):
        super(QuestionsInterface, self).__init__(parent)
        self.signal = signal
        self.result_game = result_game
        self.init_values()
        self.score = score
        self.setStyleSheet('background-image: {}'.format(Settings.dir_back, 'restar_2.jpg'))
        self.window_settings()
        self.draw_button()

        self.draw_result_game()

    def window_settings(self):
        self.setFixedSize(850, 700)

    def init_values(self):
        self.music_win = MusicWin()
        self.music_lose = MusicLose()
        self.style = Style()

    def draw_result_game(self, ):
        if self.result_game:

            # self.music_win.start()
            self.label_game_win()
        else:
            # self.music_lose.start()
            self.label_game_over()
            self.draw_label()

    def draw_label(self):
        self.score_label = QLabel('Score: ' + str(self.score), self)
        self.score_label.setStyleSheet(self.style.stylesheet_score)
        self.score_label.move(180, 386)
        self.score_label.resize(500, 60)

    def draw_button(self):
        self.button_0 = QPushButton(self)
        self.button_0.setFixedSize(0, 0)
        self.button_01 = QPushButton(self)
        self.button_01.setFixedSize(0, 0)

        self.button_1 = QPushButton('Play again', self)
        self.button_1.setStyleSheet(self.style.stylesheet_addit)
        self.button_1.clicked.connect(self.restart_game)
        self.button_1.move(180, 460)
        self.button_1.setFixedSize(500, 50)

        self.button_2 = QPushButton('Exit', self)
        self.button_2.setStyleSheet(self.style.stylesheet_addit)
        self.button_2.clicked.connect(self.close_game)

        self.button_2.move(180, 528)
        self.button_2.setFixedSize(500, 50)

    def label_game_over(self):
        self.game_over_label = QLabel("Wasted", self)
        self.game_over_label.setStyleSheet(self.style.stylesheet_game_over)
        self.game_over_label.move(168, 100)
        self.game_over_label.resize(600, 200)
        self.game_over_label.show()

    def label_game_win(self):
        self.game_win_label = QLabel("Mission passed!", self)
        self.game_win_label.setStyleSheet(self.style.stylesheet_game_win_1)
        self.game_win_label.move(130, 200)
        self.game_win_label.resize(610, 80)
        self.game_win_label.show()

        self.game_win_label_1 = QLabel("respect +" + str(self.score), self)
        self.game_win_label_1.setStyleSheet(self.style.stylesheet_game_win_2)
        self.game_win_label_1.move(240, 280)
        self.game_win_label_1.resize(600, 80)
        self.game_win_label_1.show()

    def close_this(self):
        self.close()

    def restart_game(self):

        self.close_this()
        self.signal.restart_signal.emit()

    def close_game(self):

        self.close_this()
        self.signal.closed_signal.emit()

    def closeEvent(self, event):
        self.signal.closed_signal.emit()
