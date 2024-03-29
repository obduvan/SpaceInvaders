
from os.path import join

from PyQt5.QtCore import QThread
from settings import Settings



class MusicBackground(QThread):
    def __init__(self):
        super(MusicBackground, self).__init__()
    def run(self):
        default_speaker = sc.default_speaker()
        samples, samplerate = sf.read(join(Settings.dir_music, 'back_3.wav'))
        default_speaker.play(samples, samplerate=samplerate)



class MusicShootEnem(QThread):
    def __init__(self):
        super(MusicShootEnem, self).__init__()

    def run(self):
        default_speaker = sc.default_speaker()
        samples, samplerate = sf.read(join(Settings.dir_music, 'cponk.wav'))
        default_speaker.play(samples, samplerate=samplerate)



class MusicWin(QThread):
    def __init__(self):
        super(MusicWin, self).__init__()

    def run(self):
        default_speaker = sc.default_speaker()
        samples, samplerate = sf.read(join(Settings.dir_music, 'win.wav'))
        default_speaker.play(samples, samplerate=samplerate)



class MusicShoot(QThread):
    def __init__(self):
        super(MusicShoot, self).__init__()

    def run(self):
        default_speaker = sc.default_speaker()
        samples, samplerate = sf.read(join(Settings.dir_music, 'blaster_2.wav'))
        default_speaker.play(samples, samplerate=samplerate)



class MusicKill(QThread):
    def __init__(self):
        super(MusicKill, self).__init__()

    def run(self):
        default_speaker = sc.default_speaker()
        samples, samplerate = sf.read(join(Settings.dir_music, 'kill.wav'))
        default_speaker.play(samples, samplerate=samplerate)



class MusicLose(QThread):
    def __init__(self):
        super(MusicLose, self).__init__()

    def run(self):
        default_speaker = sc.default_speaker()
        samples, samplerate = sf.read(join(Settings.dir_music, 'lose.wav'))
        default_speaker.play(samples, samplerate=samplerate)
