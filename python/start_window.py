import sys
from PyQt5.QtWidgets import *
from game_events import GameEvents

"""Здесь в будущем будет стартовое меню, если я соображу, как все
 приложение в одном окне уместить, если можно ли так вообще в PyQt"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameEvents()
    # window = StartWindow() # сообственно стартовое окно, которого нет :(
    window.show()
    app.exec_()
