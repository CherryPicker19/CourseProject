from PySide6.QtWidgets import QPushButton, QDialog, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QRunnable, QThreadPool, Slot
from chess import ChessSolver
from board_view import PIECE_COLOR, ATTACKED_TILE_COLOR, PIECE_AUTO_COLOR, BoardView

class ShowBoardWidget(QDialog):
    def __init__(self, parent):
        """
        Initialization of window with board with first solution.
        :param parent: Parent class
        """
        super().__init__(parent)
        self.setWindowTitle("Show Board")
        self.parent = parent
        self.size = parent.board_size
        self.chess = ChessSolver(parent.board_size)
        self.amount = parent.amount
        self.placed_pieces = self.parent.placed_pieces.copy()
        self.tiles_under_attack = self.parent.tiles_under_attack.copy()

        self.board_view = BoardView(parent.board_size, lambda x, y: None)
        self.tiles = self.board_view.get_board()

        self.chess.place_pieces(self.placed_pieces)
        solution = self.chess.compute(self.amount, 1)
        auto_pieces = list(filter(lambda piece: piece not in self.placed_pieces, solution))
        c1 = ChessSolver(self.size)
        for i in auto_pieces:
            moves = c1.place_piece(i[0], i[1])
            self.tiles[i[0]][i[1]].setBrush(PIECE_AUTO_COLOR)
            for j in moves:
                self.tiles[j[0]][j[1]].setBrush(ATTACKED_TILE_COLOR)

        for i in self.placed_pieces:
            moves = c1.place_piece(i[0], i[1])
            self.tiles[i[0]][i[1]].setBrush(PIECE_COLOR)
            for j in moves:
                self.tiles[j[0]][j[1]].setBrush(ATTACKED_TILE_COLOR)

        # compute and write to file button
        self.write_bt = QPushButton("Write to File")
        self.write_bt.clicked.connect(self.write_bt_clicked)

        # close button
        self.close_bt = QPushButton("Close")
        self.close_bt.clicked.connect(self.close)

        layout_board = QHBoxLayout()
        layout_board.addWidget(self.board_view)

        layout_bts = QHBoxLayout()
        layout_bts.addWidget(self.write_bt)
        layout_bts.addWidget(self.close_bt)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_board)
        layout_main.addLayout(layout_bts)
        self.setLayout(layout_main)

        self.threadpool = QThreadPool()

    def write_bt_clicked(self):
        """
        Called upon user clicking write button.
        :return: None
        """
        worker = ChessWorker(self.parent.board_size, self.placed_pieces, self.amount)
        self.threadpool.start(worker)

class ChessWorker(QRunnable):
    def __init__(self, dimensions, placed_pieces, amount):
        """
        Initializing worker class, method of which will be executed in other thread.
        :param dimensions: Size of a board
        :param placed_pieces: List of placed pieces on a board
        :param amount: Amount of pieces, that need to be placed
        """
        super().__init__()
        self.chess = ChessSolver(dimensions)
        for i in placed_pieces:
            self.chess.place_piece(i[0], i[1])
        self.amount = amount

    @Slot()
    def run(self):
        """
        Called in another thread. Writing chess solutions in a file.
        :return: None
        """
        self.chess.compute(self.amount)
        dlg = QDialog()
        dlg.setFixedSize(300, 70)
        lb = QLabel("Writing to the file is completed")
        lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bt1 = QPushButton("Ok")
        bt1.clicked.connect(dlg.close)
        layout = QVBoxLayout()
        layout.addWidget(lb)
        layout.addWidget(bt1)
        dlg.setLayout(layout)
        dlg.exec()

