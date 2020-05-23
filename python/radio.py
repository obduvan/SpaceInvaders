from PyQt5.QtCore import QThread
from playsound import playsound
from os.path import join
from settings import Settings


class MusicBackground(QThread):
    def __init__(self):
        super(MusicBackground, self).__init__()

    def run(self):
        playsound(join(Settings.dir_music, 'back_2.mp3'))


class MusicShootEnem(QThread):
    def __init__(self):
        super(MusicShootEnem, self).__init__()

    def run(self):
        playsound(join(Settings.dir_music, 'cponk.mp3'))


class MusicWin(QThread):
    def __init__(self):
        super(MusicWin, self).__init__()

    def run(self):
        playsound(join(Settings.dir_music, 'win.mp3'))


class MusicShoot(QThread):
    def __init__(self):
        super(MusicShoot, self).__init__()

    def run(self):
        playsound(join(Settings.dir_music, 'blaster.mp3'))


class MusicKill(QThread):
    def __init__(self):
        super(MusicKill, self).__init__()

    def run(self):
        playsound(join(Settings.dir_music, 'kill.mp3'))


class MusicLose(QThread):
    def __init__(self):
        super(MusicLose, self).__init__()

    def run(self):
        playsound(join(Settings.dir_music, 'lose.mp3'))
