from PyQt5.QtWidgets import QWidget


class Style(QWidget):
    def __init__(self):
        super(Style, self).__init__()
        self.styles()
        self.draw_background()

    def draw_background(self):
        """Отрисовка заднего фона"""

        self.setStyleSheet("background-color:  #151515")

    def styles(self):
        """Стили программы"""

        self.stylesheet = """
            QLabel
            {
                font: Lucida Console;
                color: #AC02E7;
                font-size: 30px;
            }
            """

        self.stylesheet_addit = """
            QPushButton
            {
                font: Gill Sans;
                color: #191616;
                font-size: 22px;             
                font-weight: bold;
                border-radius: 7px;          
            }
            
            QPushButton:hover { background-color: #C665C7 }
            QPushButton:!hover { background-color: #904891 }
            QPushButton:pressed { background-color: #C665C7 }
            """

        self.stylesheet_score = """
            QLabel
            {
                font: Lucida Console;
                color: #AC02E7;
                font-size: 47px;
                font-weight: bold;       
            }
            """

        self.stylesheet_game_over = """
            QLabel
            {
                font: Lucida Console;
                color: #c63232;
                font-size: 150px;
                font-weight: bold;
            }
            """

        self.stylesheet_game_win_1 = """
           QLabel
           {
               font: Lucida Console;
               color: #faa701;
               font-size: 80px;
               font-weight: bold;
           }
           """

        self.stylesheet_game_win_2 = """
           QLabel
           {
               font: Lucida Console;
               color: #dfdcd6;
               font-size: 70px;
               font-weight: bold;
           }
           """
