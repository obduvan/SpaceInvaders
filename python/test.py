import unittest

from PyQt5.uic.properties import QtCore
from enemies import Enemies
from start import StartInteraface
from game_events import GameEvents
from settings import Game
from event_checker import EventChecker


class BulletEnemiesTest(unittest.TestCase):
    def setUp(self):
        self.game_ev = EventChecker()

    def test_shot_registration_True(self):
        coordinates_true = [[(1, 1), (4, 4), (2, 2), (3, 3)],
                            [(10, 20), (20, 10), (15, 15), (30, 30)],
                            [(10, 20), (20, 10), (19, 19), (30, 30)],
                            [(10, 20), (20, 10), (18, 18), (3990, 30)],
                            [(410, 570), (470, 630), (467, 623), (472, 645)],
                            [(505, 570), (565, 630), (507, 619), (512, 641)],
                            [(300, 100), (346, 138), (313, 137), (318, 159)],
                            [(1, 31), (32, 3), (1, 2), (311, 31)]]

        answers = [True] * 8
        for i in range(len(answers)):
            self.assertEqual(answers[i], self.game_ev.shot_registration(coordinates_true[i][0],
                                                                         coordinates_true[i][1],
                                                                         coordinates_true[i][2],
                                                                         coordinates_true[i][3]))

        return

    def test_shot_registration_False(self):
        coordinates_false = [[(10, 230), (20, 120), (15, 11), (1, 1)],
                             [(10, 20), (20, 10), (15, 11), (1, 1)],
                             [(100, 100), (4, 4), (2, 2), (3, 3)],
                             [(100, 100), (32, 332), (90, 90), (32, 321)],
                             [(100, 3220), (32, 33322), (90, 90), (312, 321)],
                             [(100, 3220), (32, 3), (9320, 9032), (312, 3221)],
                             [(1, 31), (32, 3), (1, 32), (311, 31)]]
        answers = [False] * 7

        for i in range(len(answers)):
            self.assertEqual(answers[i], self.game_ev.shot_registration(coordinates_false[i][0],
                                                                         coordinates_false[i][1],
                                                                         coordinates_false[i][2],
                                                                         coordinates_false[i][3]))

    def test_stop_game_lives(self):
        for i in range(3):
            self.game_ev.count_lives()
        self.assertEqual(True, self.game_ev.stop_game)
        self.assertEqual(0, self.game_ev.lives)

    def test_stop_game_False(self):
        for i in range(2):
            self.game_ev.count_lives()
        self.assertEqual(False, self.game_ev.stop_game)

    def test_count_score(self):
        self.game_ev = EventChecker()

        for i in range(50):
            self.game_ev.count_score(20)
        self.assertEqual(1000, self.game_ev.score)


if __name__ == '__main__':
    unittest.main()
