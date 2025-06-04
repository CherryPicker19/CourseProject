from PySide6.QtWidgets import QPushButton, QDialog, QGridLayout, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QBrush
from PySide6.QtCore import Qt
from chess import ChessSolver
from board_view import BoardView, PIECE_COLOR, TILE_COLOR, ATTACKED_TILE_COLOR

class PlacePiecesWidget(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Place Pieces")
        self.parent = parent
        self.chess = ChessSolver(parent.board_size)

        self.placed_pieces = self.parent.placed_pieces.copy()
        self.tiles_under_attack = self.parent.tiles_under_attack.copy()

        self.board_view = BoardView(parent.board_size, self.tile_clicked)
        self.tiles = self.board_view.get_board()

        for i in self.placed_pieces:
            moves = self.chess.place_piece(i[0], i[1])
            self.tiles[i[0]][i[1]].setBrush(PIECE_COLOR)
            for j in moves:
                self.tiles[j[0]][j[1]].setBrush(ATTACKED_TILE_COLOR)

        layout_board = QGridLayout()
        layout_board.addWidget(self.board_view)
        layout_buttons = QHBoxLayout()
        self.accept_bt = QPushButton("Accept")
        self.accept_bt.clicked.connect(self.accept_bt_clicked)
        layout_buttons.addWidget(self.accept_bt)

        self.close_bt = QPushButton("Cancel")
        self.close_bt.clicked.connect(self.close)
        layout_buttons.addWidget(self.close_bt)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_board)
        layout_main.addLayout(layout_buttons)
        self.setLayout(layout_main)

    def tile_clicked(self, x, y):
        board = self.chess.board
        if self.tiles[x][y].is_LMB and (not((x, y) in self.placed_pieces) or not((x,y) in self.tiles_under_attack)):
            self.tiles[x][y].setBrush(PIECE_COLOR)
            moves = self.chess.place_piece(x, y)
            self.tiles_under_attack.extend(moves)
            self.placed_pieces.append((x, y))
            for i in moves:
                self.tiles[i[0]][i[1]].setBrush(ATTACKED_TILE_COLOR)

        elif not self.tiles[x][y].is_LMB and ((x, y) in self.placed_pieces or not (x, y) in self.tiles_under_attack):
            self.tiles[x][y].setBrush(TILE_COLOR)
            moves = self.chess.remove_piece(x, y)
            self.placed_pieces.remove((x, y))
            for i in moves:
                if board[i[0]][i[1]] == 0:
                    self.tiles[i[0]][i[1]].setBrush(TILE_COLOR)
                    self.tiles_under_attack.remove((i[0], i[1]))
        elif (x, y) in self.tiles_under_attack:
            return None

        else:
            return None

    def accept_bt_clicked(self):
        self.parent.tiles_under_attack = self.tiles_under_attack
        self.parent.placed_pieces = self.placed_pieces
        self.parent.chess = self.chess
        self.close()
