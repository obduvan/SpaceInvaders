class ShotReg:
    @staticmethod
    def shot_registration(a, b, a1, b1):
        return (b[0] > a1[0] and b[0] < b1[0] and b[1] > a1[1] and b[1] < b1[1]) or (
                b1[0] > a[0] and b1[0] < b[0] and a1[1] > a[1] and a1[1] < b[1]) or (
                a[0] > a1[0] and a[0] < b1[0] and a[1] > a1[1] and a[1] < b1[1]) or (
                b[0] > a1[0] and b[0] < b1[0] and a[1] > a1[1] and a[1] < b1[1])


class EventChecker:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.stop_game = False

    def count_score(self, kill):
        self.score += kill

    def count_lives(self):
        self.lives -= 1
        if self.lives == 0:
            self.stop_game = True
