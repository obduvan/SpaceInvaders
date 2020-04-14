from PyQt5.QtCore import *


class Signals(QObject):
    """Сигналы, используемые в многопоточности"""

    def __init__(self):
        super(Signals, self).__init__()

    bullet_signal = pyqtSignal(object, int, int)
    enemies_signal = pyqtSignal(int, int, int, int)
    enemy_random_signal = pyqtSignal(int, int)
    enemy_bullet_signal = pyqtSignal(object, int, int)
