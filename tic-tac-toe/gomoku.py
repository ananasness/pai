from random import randint


class Gomoku:
    def __init__(self, n_cells=8):
        self.n_cells = n_cells
        self.player_1_piece = '❌'
        self.player_2_piece = '⭕️'
        self.empty_piece = '.'
        self.state = [[self.empty_piece for _ in range(self.n_cells)]
                      for _ in range(self.n_cells)]

    def play(self, x: int, y: int):
        if not self.is_move_valid(x, y):
            # status = self.check_all()
            # if status != 0:
            #     return self.state, status

            return self.state, 4
        else:
            self.state[y][x] = self.player_1_piece

            status = self.check_all()
            if status != 0:
                return self.state, status

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

            status = self.check_all()
            if status != 0:
                return self.state, status

            return self.state, 0

    def is_move_valid(self, x, y):
        if 0 <= x <= self.n_cells - 1 and \
                0 <= y <= self.n_cells - 1 and \
                self.state[y][x] == self.empty_piece:
            return True
        else:
            return False

    def check_row(self, x, y, piece):
        if self.state[y][x] == piece and \
                self.state[y][x + 1] == piece and \
                self.state[y][x + 2] == piece and \
                self.state[y][x + 3] == piece and \
                self.state[y][x + 4] == piece:
            return True
        else:
            return False

    def check_col(self, x, y, piece):
        if self.state[y][x] == piece and \
                self.state[y + 1][x] == piece and \
                self.state[y + 2][x] == piece and \
                self.state[y + 3][x] == piece and \
                self.state[y + 4][x] == piece:
            return True
        else:
            return False

    def check_main_diag(self, x, y, piece):
        if self.state[y][x] == piece and \
                self.state[y + 1][x + 1] == piece and \
                self.state[y + 2][x + 2] == piece and \
                self.state[y + 3][x + 3] == piece and \
                self.state[y + 4][x + 4] == piece:
            return True
        else:
            return False

    def check_anti_diag(self, x, y, piece):
        if self.state[y][x] == piece and \
                self.state[y + 1][x - 1] == piece and \
                self.state[y + 2][x - 2] == piece and \
                self.state[y + 3][x - 3] == piece and \
                self.state[y + 4][x - 4] == piece:
            return True
        else:
            return False

    def check_all(self):
        for x in range(self.n_cells - 4):
            for y in range(self.n_cells):
                if self.check_row(x, y, self.player_1_piece):
                    return 1
                if self.check_row(x, y, self.player_2_piece):
                    return 2

        for x in range(self.n_cells):
            for y in range(self.n_cells - 4):
                if self.check_col(x, y, self.player_1_piece):
                    return 1
                if self.check_col(x, y, self.player_2_piece):
                    return 2

        for x in range(self.n_cells - 4):
            for y in range(self.n_cells - 4):
                if self.check_main_diag(x, y, self.player_1_piece):
                    return 1
                if self.check_main_diag(x, y, self.player_2_piece):
                    return 2

        for x in range(4, self.n_cells):
            for y in range(self.n_cells - 4):
                if self.check_anti_diag(x, y, self.player_1_piece):
                    return 1
                if self.check_anti_diag(x, y, self.player_2_piece):
                    return 2

        n_empty_cells = 0
        for x in range(self.n_cells):
            for y in range(self.n_cells):
                if self.state[y][x] == self.empty_piece:
                    n_empty_cells += 1

        if n_empty_cells == 0:
            return 3

        return 0

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
    state, status = game.play(0, 0)
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
    state, status = game.play(1, 0)
    print(game, status)
    state, status = game.play(1, 6)
    print(game, status)
    state, status = game.play(1, 7)
    print(game, status)

    state, status = game.play(2, 0)
    print(game, status)
    state, status = game.play(2, 1)
    print(game, status)
    state, status = game.play(2, 0)
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
