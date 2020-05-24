from PyQt5.QtCore import QObject, pyqtSignal


class Signals(QObject):
    """Сигналы, используемые в многопоточности"""

    def __init__(self):
        super(Signals, self).__init__()

    bullet_signal = pyqtSignal(object, int, int)
    enemies_signal = pyqtSignal(int, int, int, int)
    enemy_random_signal = pyqtSignal(int, int, int)
    enemy_bullet_signal = pyqtSignal(object, int, int)
    check_live_enem_signal = pyqtSignal(int, int)
    reverse_live_enem_signal = pyqtSignal(bool)


    player_on_shoot_draw = pyqtSignal(object)
    player_on_shoot_died = pyqtSignal()
    jesus = pyqtSignal()
    reverse_bullet_player = pyqtSignal(bool)
    bullet_position_reverse = pyqtSignal(int, int)
    hide_enemies_signal = pyqtSignal()
    stop_game_singal = pyqtSignal(bool, bool)
    restart_signal = pyqtSignal()
    closed_signal = pyqtSignal()
    bullet_state_shoot = pyqtSignal(int)
