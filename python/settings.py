from os.path import join
from os import path


class Settings:
    """Настройки проекта"""

    base_dir = path.dirname(path.dirname(__file__))  # путь проекта
    dir_graphics = join(base_dir, "graphics")  # папка графики
    dir_bullets_graphics = join(dir_graphics, "booms")  # папка с пулями
    dir_enemies_graphics = join(dir_graphics, "enemies")  # папка с захватчиками
    dir_interface_graphics = join(dir_graphics, "interface")  # папка с графикой интерфейса
    dir_player_graphics = join(dir_graphics, "player")  # пака с графикой главного игрока
    dir_defenders = join(dir_graphics, 'defenders')

    dir_logo = join(dir_graphics, 'logo')
    dir_scripts = join(base_dir, 'python')
    dir_back = join(dir_scripts, 'menu')
    dir_music = join(base_dir, 'shanson')


class Game:
    def __init__(self, enemies, time, step_time, limit_step):
        self.enemies = enemies
        self.time_enemies = time
        self.step_time = step_time
        self.limit_step = limit_step
