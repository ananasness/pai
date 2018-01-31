from random import randint


class Gomoku:
    def __init__(self, n_cols=8, n_rows=8):
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.state = [["." for _ in range(0, self.n_cols)] for _ in range(0, self.n_cols)]

    def play(self, x: int, y: int):
        if not self.is_move_valid(x, y):
            return self.state
        else:
            self.state[y][x] = "X"
            while True:
                bx = randint(0, 7)
                by = randint(0, 7)
                if self.state[by][bx] == '.':
                    self.state[by][bx] = 'O'
                    break

            return self.state

    def is_move_valid(self, x, y):
        if 0 <= x <= self.n_cols - 1 and 0 <= y <= self.n_rows - 1 and self.state[y][x] == '.':
            return True
        else:
            return False

    def __str__(self):
        return str(self.state).replace('], [', '],\n [')


if __name__ == '__main__':
    game = Gomoku()
    print(game)
    game.play(0, 0)
    print(game)
    game.play(6, 2)
    print(game)
    game.play(6, 5)
    print(game)
    game.play(7, 7)
    print(game)
    game.play(2, 3)
    print(game)
