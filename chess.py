def read_input(filename: str) -> tuple:
    with open(filename, 'r') as f:
        n, l, k = map(int, f.readline().strip().split())
        pieces = [tuple(map(int, f.readline().strip().split())) for _ in range(k)]
    return n, l, pieces

class Chess:
    def __init__(self, dimensions: int, board: list[list[int]], _moves: tuple[tuple[int, int], ...]=None):
        """
        Initializing class with basic chess functions
        :param dimensions: Size of the board
        :param board: Two-dimensional list
        :param _moves: Moves of pieces that can be placed on the board
        """
        if _moves is None:
            self.__moves = (
            (0, -1), (0, 1), (3, 0), (-3, 0), (0, -3), (0, 3), (-1, -2), (-1, 2), (-1, 0), (1, -2), (1, 2), (1, 0),
            (-2, -1),
            (-2, 1), (2, -1), (2, 1))
        else:
            self.__moves = _moves

        self.__dimensions = dimensions
        self.__board = board
        self._placed_pieces = []

    def print(self) -> None:
        """
        Prints board beautifully
        :return: None
        """
        s = str(self.__board).replace('], [', '] \n [').replace(', ', ' ').replace('[', '').replace(']', '') + '\n'
        res = ""
        for i in s.split(sep=" "):
            if i == '\n':
                res = res + '\n'
            elif int(i) == -1:
                res = res + '#'
            elif int(i) > 0:
                res = res + '*'
            elif int(i) == 0:
                res = res + '0'
        print(res + '\n')

    @staticmethod
    def create_board(dimensions: int) -> list[list[int]]:
        """
        Creates two-dimensional list
        :param dimensions: Size of the board
        :return: two-dimensional list
        """
        return [[0 for i in range(dimensions)] for j in range(dimensions)]

    def __change_piece(self, x: int, y: int, action: bool) -> list[tuple[int, int]]: # action: True - place; False - remove
        """
        Places or removes piece. action - True for placing piece, otherwise removes piece
        :param x: X coordinate
        :param y: Y coordinate
        :param action: True - place piece. False - remove piece
        :return: list with tuples, that contain x and y coordinates of attacked tiles
        """
        coord_under_atck = []
        if x > self.__dimensions - 1 or y > self.__dimensions - 1:
            raise IndexError("Index is out of range!")
        self.__board[x][y] = action * -1
        action = (2 * action) - 1 # returns 1 if action is True; return -1 if action is False
        for i in self.__moves:
            if x + i[0] < 0 or y + i[1] < 0 or x + i[0] > self.__dimensions - 1 or y + i[1] > self.__dimensions - 1:
                continue
            else:
                self.__board[x + i[0]][y + i[1]] += action
                coord_under_atck.append((x + i[0], y + i[1]))
        return coord_under_atck

    def place_piece(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Places piece on the board.
        :param x: X coordinate
        :param y: Y coordinate
        :return: list containing tuples, with x and y coordinates of attacks
        """
        if self.__board[x][y] == 0:
            self._placed_pieces.append((x, y))
            coord = self.__change_piece(x, y, True)
            return coord
        return []

    def place_pieces(self, pieces: list[tuple[int, int], ]) -> None:
        """
        Places a bunch of pieces on the board
        :param pieces: List that contains coordinates of pieces
        :return: List that contains tuples with coordinates of piece's attacks
        """
        for i in pieces:
            self.place_piece(i[0], i[1])

    def remove_piece(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Removes piece of the board
        :param x: X coordinate
        :param y: Y coordinate
        :return: List that contains tuples with coordinates of piece's removed attacks
        """
        if self.__board[x][y] == -1:
            coord = self.__change_piece(x, y, False)
            return coord
        return []

class ChessSolver(Chess):
    def __init__(self, dimensions: int, output_file: str = 'output.txt', _moves=None):
        """
        Initializing class that adds algorithm of solving chess
        :param dimensions: Size of the board
        :param output_file: File, where all solutions will be written to
        :param _moves: Moves of a piece
        """
        self.__board = self.create_board(dimensions)
        if _moves is None:
            self._moves = (
            (0, -1), (0, 1), (3, 0), (-3, 0), (0, -3), (0, 3), (-1, -2), (-1, 2), (-1, 0), (1, -2), (1, 2), (1, 0),
            (-2, -1),
            (-2, 1), (2, -1), (2, 1))
        else:
            self._moves = _moves
        super().__init__(dimensions, self.__board, self._moves)
        self.__cache = set()
        self.__cur_solution = []
        self.output_file = output_file
        self.__dimensions = dimensions
        self.__const_pieces = self._placed_pieces

    @property
    def board(self):
        return self.__board

    @property
    def pieces(self):
        return self.__const_pieces

    def __algorithm(self, x: int = 0, y: int = 0, l = 0) -> None:
        """
        Algorithm of finding and writing to the file all possible solutions
        :param x: X coordinate
        :param y: Y coordinate
        :param l: Amount of pieces that needs to be placed
        :return: None
        """
        if l == 0:
            self.__cur_solution.sort()
            cur_solution_t = tuple(self.__cur_solution)
            if cur_solution_t in self.__cache:
                return None
            self.__cache.update(cur_solution_t)
            answ = self.__const_pieces + self.__cur_solution
            for el in answ:
                self.__f.write(str(el) + " ")
            self.__f.write('\n')
            return None
        for i in range(x, self.__dimensions):
            for j in range(y if i == x else 0, self.__dimensions):
                if self.__board[i][j] == 0:
                    self.__cur_solution.append((i, j))
                    self.place_piece(i, j)
                    self.__algorithm(i, j, l - 1)
                    self.remove_piece(i, j)
                    self.__cur_solution.pop()
        return None

    def __algorithm_with_end(self, x: int = 0, y: int = 0, l = 0) -> list[tuple[int, int],]:
        """
        Algorithm that returns first found solution
        :param x: X coordinate
        :param y: Y coordinate
        :param l: Amount of pieces that needs to be placed
        :return: First found solution
        """
        if l == 0:
            self.__cur_solution.sort()
            cur_solution_t = tuple(self.__cur_solution)
            if cur_solution_t in self.__cache:
                return self.__const_pieces + self.__cur_solution
            self.__cache.update(cur_solution_t)
            answ = self.__const_pieces + self.__cur_solution
            return answ
        for i in range(x, self.__dimensions):
            for j in range(y if i == x else 0, self.__dimensions):
                if self.__board[i][j] == 0:
                    self.__cur_solution.append((i, j))
                    self.place_piece(i, j)
                    a = self.__algorithm_with_end( i, j, l - 1)
                    return a
        return []

    def compute(self, amount_of_pieces: int, end = -1) -> None | list:
        """
        Wrapper of algorithm and algorithm with first solution
        :param amount_of_pieces: Amount of pieces that needs to be placed
        :param end: if not -1 then executes algorithm of finding first solution
        :return: None or first solution
        """
        self.__const_pieces = self._placed_pieces.copy()
        self.__f = open(self.output_file, 'w')
        if amount_of_pieces > self.__dimensions * self.__dimensions:
            self.__f.write('no solutions')
            self.__f.close()
        elif end == -1:
            self.__algorithm(l=amount_of_pieces)
            self.__f.close()
        else:
            answ = self.__algorithm_with_end(end, l=amount_of_pieces)
            self.__f.close()
            return answ

if __name__ == '__main__':
    dimensions, amount_of_pieces, const_pieces = read_input("input.txt")
    chess = ChessSolver(dimensions)
    chess.place_piece(5, 5)
    a = chess.compute(1, 1)
    print(a)
    chess.print()

