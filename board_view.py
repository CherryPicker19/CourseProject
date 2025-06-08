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

# Constants
TILE_SIZE = 25
SPACING = 5
TILE_COLOR = QBrush(Qt.green)
PIECE_COLOR = QBrush(Qt.red)
PIECE_AUTO_COLOR = QBrush(Qt.blue)
ATTACKED_TILE_COLOR = QBrush(Qt.black)

class Tile(QGraphicsRectItem):
    def __init__(self, x, y, width, height, func):
        """
        Initializing Tile class.
        :param x: X coordinate
        :param y: Y coordinate
        :param width: Width of a tile
        :param height: Height of a tile
        :param func: Function that will be called upon clicking tile
        """
        super().__init__(x, y, width, height)
        self.setBrush(TILE_COLOR)
        self.is_LMB = None
        self.func = func
        self.under_attack = False

    def mousePressEvent(self, event, /):
        """
        Called upon clicking on the tile. Determines what button was clicked and changes is_LMB parameter if needed.
        :param event: An instance of QGraphicsSceneMouseEvent
        :return: None
        """
        if event.button() == Qt.MouseButton.RightButton:
            self.is_LMB = False
        elif event.button() == Qt.MouseButton.LeftButton:
            self.is_LMB = True
        self.func()
        super().mousePressEvent(event)

class BoardView(QGraphicsView):
    def __init__(self, size: int, func):
        """
        Initialization of PySide6's QGraphicsView with board and pieces placed on it.
        :param size: Size of the board
        :param func: Function that will be called upon user clicking a tile. Have to have first two parameters of x and y coordinates
        """
        super().__init__()
        self.size: int = size
        self.func = func
        self.scene: QGraphicsScene = QGraphicsScene(self)
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )
        self.board = [] # two-dimensional list, containing instances of class Tile
        for i in range(size):
            a = []
            for j in range(size):
                func = partial(self.func, i, j)
                rect = Tile(j*(TILE_SIZE+SPACING), i*(TILE_SIZE+SPACING), TILE_SIZE, TILE_SIZE, func)
                a.append(rect)
                self.scene.addItem(rect)
            self.board.append(a)
        self.setScene(self.scene)

    def get_board(self) -> list[list[Tile, ], ]:
        """
        :return: Board
        """
        return self.board

if __name__ == '__main__':
    ap = QApplication()
    window = BoardView(10, lambda x,y: 0)
    window.show()
    ap.exec()
