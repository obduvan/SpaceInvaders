import os
from os import path


class Settings:
    """Настройки проекта"""

    base_dir = os.path.dirname(os.path.dirname(__file__))  # путь проекта
    dir_graphics = path.join(base_dir, "graphics")  # папка графики
    dir_bullets_graphics = path.join(dir_graphics, "booms")  # папка с пулями
    dir_enemies_graphics = path.join(dir_graphics, "enemies")  # папка с захватчиками
    dir_interface_graphics = path.join(
        dir_graphics, "interface"
    )  # папка с графикой интерфейса
    dir_player_graphics = path.join(
        dir_graphics, "player"
    )  # пака с графикой главного игрока
