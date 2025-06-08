from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QDialog
)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIntValidator
from chess import ChessSolver
from place_pieces_dialog import PlacePiecesWidget
from show_board_dialog import ShowBoardWidget
import sys

MAIN_WINDOW_SIZE = QSize(300, 200)

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialization of main window class.
        """
        super().__init__()

        self.board_size: int
        self.board_size_lck = True
        self.amount: int
        self.amount_lck = True

        self.chess: ChessSolver
        self.placed_pieces = []
        self.tiles_under_attack = []

        self.setWindowTitle("ThinkChess")

        # set window size
        self.setFixedSize(MAIN_WINDOW_SIZE)

        validator = QIntValidator(1, 20, self)
        # size of the board
        self.size_label = QLabel("Input size of the board:")
        self.size_input = QLineEdit()
        self.size_input.textEdited.connect(self.size_inputed)
        self.size_input.setValidator(validator)

        layout_size = QHBoxLayout()
        layout_size.addWidget(self.size_label)
        layout_size.addWidget(self.size_input)

        # amount of pieces
        validator2 = QIntValidator(1, 20*20, self)
        self.amount_label = QLabel("Input amount of pieces")
        self.amount_input = QLineEdit()
        self.amount_input.textEdited.connect(self.amount_inputed)
        self.amount_input.setValidator(validator2)

        layout_pieces = QHBoxLayout()
        layout_pieces.addWidget(self.amount_label)
        layout_pieces.addWidget(self.amount_input)

        layout_buttons = QHBoxLayout()
        # place pieces button
        self.place_pieces_bt = QPushButton("Place Pieces")
        self.place_pieces_bt.setDisabled(True)
        self.place_pieces_bt.clicked.connect(self.place_pieces_bt_clicked)
        layout_buttons.addWidget(self.place_pieces_bt)

        # show board button
        self.show_board_bt = QPushButton("Show Board")
        self.show_board_bt.setDisabled(True)
        self.show_board_bt.clicked.connect(self.show_board_bt_clicked)
        layout_buttons.addWidget(self.show_board_bt)

        # exit button
        self.exit_bt = QPushButton("Exit")
        self.exit_bt.clicked.connect(self.close)
        layout_buttons.addWidget(self.exit_bt)

        layout = QVBoxLayout()
        layout.addLayout(layout_size)
        layout.addLayout(layout_pieces)
        layout.addLayout(layout_buttons)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def size_inputed(self, text: str):
        """
        Called upon size text editing.
        :param text: User input
        :return: None
        """
        if text == "":
            self.board_size_lck = True
        else:
            num = int(text)
            if num > 20 or num < 1:
                self.board_size_lck = True
            else:
                self.board_size = num
                self.chess = ChessSolver(self.board_size)
                self.placed_pieces = []
                self.board_size_lck = False
        self.__unblock_bts()

    def amount_inputed(self, text):
        """
        Called upon amount text editing.
        :param text: User input
        :return: None
        """
        if text == "":
            self.amount_lck = True
        else:
            numb = int(text)
            if numb > 20 * 20 or numb < 1:
                self.amount_lck = True
            else:
                self.amount = numb
                self.amount_lck = False
        self.__unblock_bts()

    def __unblock_bts(self):
        """
        Called upon size or amount text inputting. Enables or Disables show board and place piece buttons.
        :return: None
        """
        if not self.board_size_lck and not self.amount_lck:
            self.place_pieces_bt.setDisabled(False)
            self.show_board_bt.setDisabled(False)
            self.chess = ChessSolver(self.board_size)
        else:
            self.place_pieces_bt.setDisabled(True)
            self.show_board_bt.setDisabled(True)

    def place_pieces_bt_clicked(self):
        """
        Called upon place pieces button clicked. Creates a window, where user can place chess pieces.
        :return: None
        """
        wdg = PlacePiecesWidget(self)
        wdg.exec()

    def show_board_bt_clicked(self):
        """
        Called upon show board button clicked. Creates a window, where user can see board with first solution.
        Creates a window with text: "No solution found" if no solution has been found.
        :return: None
        """
        solution = self.chess.compute(self.amount, 1)
        self.chess = ChessSolver(self.board_size)
        for i in self.placed_pieces:
            self.chess.place_piece(i[0],  i[1])
        if not solution:
            dlg = QDialog()
            dlg.setFixedSize(200, 70)
            lb = QLabel("No solution found")
            lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            b1 = QPushButton("Ok")
            b1.clicked.connect(dlg.close)
            layout = QVBoxLayout()
            layout.addWidget(lb)
            layout.addWidget(b1)
            dlg.setLayout(layout)
            dlg.exec()
        else:
            wdg = ShowBoardWidget(self)
            wdg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
