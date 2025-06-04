def read_input(filename: str) -> tuple:
    with open(filename, 'r') as f:
        n, l, k = map(int, f.readline().strip().split())
        pieces = [tuple(map(int, f.readline().strip().split())) for _ in range(k)]
    return n, l, pieces

class Chess:
    def __init__(self, dimensions: int, board: list[list[int]], _moves: tuple[tuple[int, int], ...]=None):
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
        return [[0 for i in range(dimensions)] for j in range(dimensions)]

    def __change_piece(self, x: int, y: int, action: bool) -> list[tuple[int, int]]: # action: True - place; False - remove
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
        if self.__board[x][y] == 0:
            self._placed_pieces.append((x, y))
            coord = self.__change_piece(x, y, True)
            return coord
        return []

    def place_pieces(self, pieces: list[tuple[int, int], ...]) -> None:
        for i in pieces:
            self.place_piece(i[0], i[1])

    def remove_piece(self, x: int, y: int) -> list[tuple[int, int]]:
        if self.__board[x][y] == -1:
            coord = self.__change_piece(x, y, False)
            return coord
        return []

class ChessSolver(Chess):
    def __init__(self, dimensions: int, output_file: str = 'output.txt', _moves=None):
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

    def __algorithm_with_end(self, end: int, x: int = 0, y: int = 0, l = 0) -> list | None:
        if l == 0:
            self.__cur_solution.sort()
            cur_solution_t = tuple(self.__cur_solution)
            if cur_solution_t in self.__cache:
                end += 1
                return self.__const_pieces + self.__cur_solution
            self.__cache.update(cur_solution_t)
            answ = self.__const_pieces + self.__cur_solution
            end += 1
            return answ
        for i in range(x, self.__dimensions):
            for j in range(y if i == x else 0, self.__dimensions):
                if self.__board[i][j] == 0:
                    self.__cur_solution.append((i, j))
                    self.place_piece(i, j)
                    a = self.__algorithm_with_end(end, i, j, l - 1)
                    if end == 1:
                        return a
                    self.remove_piece(i, j)
                    self.__cur_solution.pop()
        return None

    def print_solution(self) -> None:
        self.__f = open(self.output_file, 'r')
        a = self.__f.readline()
        if a == 'no solutions':
            print('no solutions')
            return None
        a = str(a).strip().split(sep=' ')
        c = [ele.replace(',', '') for ele in a]
        b = [ele.replace('(', '') for ele in c]
        d = [ele.replace(')', '') for ele in b]
        p = []
        for i in range(1, len(d), 2):
            p.append((d[i - 1], d[i]))
        d = []
        for i in p:
            d.append((int(i[0]), int(i[1])))
        for i in d:
            self.place_piece(i[0], i[1])
        self.print_board()
        self.__f.close()
        for i in d:
            if i not in self.__const_pieces:
                self.remove_piece(i[0], i[1])

    def compute(self, amount_of_pieces: int, end = -1) -> None | list:
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

