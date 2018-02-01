from random import randint


class Gomoku:
    def __init__(self, n_cells=8):
        self.n_cells = n_cells
        self.player_1_piece = 'X'
        self.player_2_piece = 'O'
        self.empty_piece = '.'
        self.state = [[self.empty_piece for _ in range(self.n_cells)]
                      for _ in range(self.n_cells)]

    def play(self, x: int, y: int):
        if not self.is_move_valid(x, y):
            check_result = self.check()
            if check_result == 1 or check_result == 2:
                return self.state, check_result

            n_empty_cells = 0
            for i in range(self.n_cells):
                for j in range(self.n_cells):
                    if self.state[i][j] == self.empty_piece:
                        n_empty_cells += 1

            if n_empty_cells == 0:
                return self.state, 3

            return self.state, 4
        else:
            self.state[y][x] = self.player_1_piece
            while True:
                bx = randint(0, 7)
                by = randint(0, 7)
                if self.state[by][bx] == self.empty_piece:
                    self.state[by][bx] = self.player_2_piece
                    break

            """
            0 - continue
            1 - won player 1
            2 - won player 2 (bot)
            3 - tie
            4 - invalid move
            """

            check_result = self.check()
            if check_result == 1 or check_result == 2:
                return self.state, check_result

            n_empty_cells = 0
            for i in range(self.n_cells):
                for j in range(self.n_cells):
                    if self.state[i][j] == self.empty_piece:
                        n_empty_cells += 1

            if n_empty_cells == 0:
                return self.state, 3

            return self.state, 0

    def is_move_valid(self, x, y):
        if 0 <= x <= self.n_cells - 1 and \
                0 <= y <= self.n_cells - 1 and \
                self.state[y][x] == self.empty_piece:
            return True
        else:
            return False

    def has_record(self, y, x):
        return not self.state[y][x] == self.empty_piece

    def check_row(self, y, x):
        if self.has_record(x, y) and \
                self.has_record(x, y + 1) and \
                self.has_record(x, y + 2) and \
                self.has_record(x, y + 3) and \
                self.has_record(x, y + 4):

            if self.state[x][y] == self.player_1_piece and \
                    self.state[x][y + 1] == self.player_1_piece and \
                    self.state[x][y + 2] == self.player_1_piece and \
                    self.state[x][y + 3] == self.player_1_piece and \
                    self.state[x][y + 4] == self.player_1_piece:
                return 1

            elif self.state[x][y] == self.player_2_piece and \
                    self.state[x][y + 1] == self.player_2_piece and \
                    self.state[x][y + 2] == self.player_2_piece and \
                    self.state[x][y + 3] == self.player_2_piece and \
                    self.state[x][y + 4] == self.player_2_piece:
                return 2
        else:
            return 0

    def check_col(self, y, x):
        if self.has_record(x, y) and \
                self.has_record(x + 1, y) and \
                self.has_record(x + 2, y) and \
                self.has_record(x + 3, y) and \
                self.has_record(x + 4, y):

            if self.state[x][y] == self.player_1_piece and \
                    self.state[x + 1][y] == self.player_1_piece and \
                    self.state[x + 2][y] == self.player_1_piece and \
                    self.state[x + 3][y] == self.player_1_piece and \
                    self.state[x + 4][y] == self.player_1_piece:
                return 1

            elif self.state[x][y] == self.player_2_piece and \
                    self.state[x + 1][y] == self.player_2_piece and \
                    self.state[x + 2][y] == self.player_2_piece and \
                    self.state[x + 3][y] == self.player_2_piece and \
                    self.state[x + 4][y] == self.player_2_piece:
                return 2
        else:
            return 0

    def check_up(self, y, x):
        if self.has_record(x, y) and \
                self.has_record(x + 1, y + 1) and \
                self.has_record(x + 2, y + 2) and \
                self.has_record(x + 3, y + 3) and \
                self.has_record(x + 4, y + 4):

            if self.state[x][y] == self.player_1_piece and \
                    self.state[x + 1][y + 1] == self.player_1_piece and \
                    self.state[x + 2][y + 2] == self.player_1_piece and \
                    self.state[x + 3][y + 3] == self.player_1_piece and \
                    self.state[x + 4][y + 4] == self.player_1_piece:
                return 1

            elif self.state[x][y] == self.player_2_piece and \
                    self.state[x + 1][y + 1] == self.player_2_piece and \
                    self.state[x + 2][y + 2] == self.player_2_piece and \
                    self.state[x + 3][y + 3] == self.player_2_piece and \
                    self.state[x + 4][y + 4] == self.player_2_piece:
                return 2
        else:
            return 0

    def check_down(self, y, x):
        if self.has_record(x, y) and \
                self.has_record(x + 1, y - 1) and \
                self.has_record(x + 2, y - 2) and \
                self.has_record(x + 3, y - 3) and \
                self.has_record(x + 4, y - 4):

            if self.state[x][y] == self.player_1_piece and \
                    self.state[x + 1][y - 1] == self.player_1_piece and \
                    self.state[x + 2][y - 2] == self.player_1_piece and \
                    self.state[x + 3][y - 3] == self.player_1_piece and \
                    self.state[x + 4][y - 4] == self.player_1_piece:
                return 1

            elif self.state[x][y] == self.player_2_piece and \
                    self.state[x + 1][y - 1] == self.player_2_piece and \
                    self.state[x + 2][y - 2] == self.player_2_piece and \
                    self.state[x + 3][y - 3] == self.player_2_piece and \
                    self.state[x + 4][y - 4] == self.player_2_piece:
                return 2

        else:
            return 0

    def check(self):
        for i in range(self.n_cells):
            for j in range(self.n_cells - 4):
                result = self.check_row(j, i)
                if result != 0:
                    return result

        for i in range(self.n_cells - 4):
            for j in range(self.n_cells):
                result = self.check_col(j, i)
                if result != 0:
                    return result

        for i in range(self.n_cells - 4):
            for j in range(self.n_cells - 4):
                result = self.check_up(j, i)
                if result != 0:
                    return result

        for i in range(self.n_cells - 4):
            for j in range(4, self.n_cells):
                result = self.check_down(j, i)
                if result != 0:
                    return result

    def __str__(self):
        return str(self.state).replace('], [', '],\n [')


if __name__ == '__main__':
    game = Gomoku()

    state, status = game.play(0, 0)
    print(game, status)
    state, status = game.play(0, 1)
    print(game, status)
    state, status = game.play(0, 2)
    print(game, status)
    state, status = game.play(0, 3)
    print(game, status)
    state, status = game.play(0, 4)
    print(game, status)
    state, status = game.play(0, 5)
    print(game, status)
    state, status = game.play(0, 6)
    print(game, status)
    state, status = game.play(0, 7)
    print(game, status)

    state, status = game.play(1, 0)
    print(game, status)
    state, status = game.play(1, 1)
    print(game, status)
    state, status = game.play(1, 2)
    print(game, status)
    state, status = game.play(1, 3)
    print(game, status)
    state, status = game.play(1, 4)
    print(game, status)
    state, status = game.play(1, 5)
    print(game, status)
    state, status = game.play(1, 6)
    print(game, status)
    state, status = game.play(1, 7)
    print(game, status)

    state, status = game.play(2, 0)
    print(game, status)
    state, status = game.play(2, 1)
    print(game, status)
    state, status = game.play(2, 2)
    print(game, status)
    state, status = game.play(2, 3)
    print(game, status)
    state, status = game.play(2, 4)
    print(game, status)
    state, status = game.play(2, 5)
    print(game, status)
    state, status = game.play(2, 6)
    print(game, status)
    state, status = game.play(2, 7)
    print(game, status)

    state, status = game.play(3, 0)
    print(game, status)
    state, status = game.play(3, 1)
    print(game, status)
    state, status = game.play(3, 2)
    print(game, status)
    state, status = game.play(3, 3)
    print(game, status)
    state, status = game.play(3, 4)
    print(game, status)
    state, status = game.play(3, 5)
    print(game, status)
    state, status = game.play(3, 6)
    print(game, status)
    state, status = game.play(3, 7)
    print(game, status)

    state, status = game.play(4, 0)
    print(game, status)
    state, status = game.play(4, 1)
    print(game, status)
    state, status = game.play(4, 2)
    print(game, status)
    state, status = game.play(4, 3)
    print(game, status)
    state, status = game.play(4, 4)
    print(game, status)
    state, status = game.play(4, 5)
    print(game, status)
    state, status = game.play(4, 6)
    print(game, status)
    state, status = game.play(4, 7)
    print(game, status)

    state, status = game.play(5, 0)
    print(game, status)
    state, status = game.play(5, 1)
    print(game, status)
    state, status = game.play(5, 2)
    print(game, status)
    state, status = game.play(5, 3)
    print(game, status)
    state, status = game.play(5, 4)
    print(game, status)
    state, status = game.play(5, 5)
    print(game, status)
    state, status = game.play(5, 6)
    print(game, status)
    state, status = game.play(5, 7)
    print(game, status)

    state, status = game.play(6, 0)
    print(game, status)
    state, status = game.play(6, 1)
    print(game, status)
    state, status = game.play(6, 2)
    print(game, status)
    state, status = game.play(6, 3)
    print(game, status)
    state, status = game.play(6, 4)
    print(game, status)
    state, status = game.play(6, 5)
    print(game, status)
    state, status = game.play(6, 6)
    print(game, status)
    state, status = game.play(6, 7)
    print(game, status)

    state, status = game.play(7, 0)
    print(game, status)
    state, status = game.play(7, 1)
    print(game, status)
    state, status = game.play(7, 2)
    print(game, status)
    state, status = game.play(7, 3)
    print(game, status)
    state, status = game.play(7, 4)
    print(game, status)
    state, status = game.play(7, 5)
    print(game, status)
    state, status = game.play(7, 6)
    print(game, status)
    state, status = game.play(7, 7)
    print(game, status)
