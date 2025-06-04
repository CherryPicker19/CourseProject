from PySide6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QSizePolicy
)
from PySide6.QtGui import QBrush
from PySide6.QtCore import Qt
from functools import partial

TILE_SIZE = 25
TILE_COLOR = QBrush(Qt.green)
PIECE_COLOR = QBrush(Qt.red)
PIECE_AUTO_COLOR = QBrush(Qt.blue)
ATTACKED_TILE_COLOR = QBrush(Qt.black)

class Tile(QGraphicsRectItem):
    def __init__(self, x, y, width, height, func):
        super().__init__(x, y, width, height)
        self.setBrush(TILE_COLOR)
        self.is_LMB = None
        self.func = func
        self.under_attack = False

    def mousePressEvent(self, event, /):
        if event.button() == Qt.MouseButton.RightButton:
            self.setBrush(TILE_COLOR)
            self.is_LMB = False
        elif event.button() == Qt.MouseButton.LeftButton:
            self.setBrush(PIECE_COLOR)
            self.is_LMB = True
        self.func()
        super().mousePressEvent(event)

class BoardView(QGraphicsView):
    def __init__(self, size: int, func):
        super().__init__()

        self.size = size
        self.func = func
        self.scene = QGraphicsScene(self)
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )
        self.board = []
        for i in range(size):
            a = []
            for j in range(size):
                func = partial(self.func, i, j)
                rect = Tile(j*(TILE_SIZE+1), i*(TILE_SIZE+1), TILE_SIZE, TILE_SIZE, func)
                a.append(rect)
                self.scene.addItem(rect)
            self.board.append(a)
        self.setScene(self.scene)
        print(self.board)

    def get_board(self):
        return self.board


if __name__ == '__main__':
    ap = QApplication()
    window = W()
    window.show()
    ap.exec()