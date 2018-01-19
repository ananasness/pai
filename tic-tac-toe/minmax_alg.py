import numpy as np

lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


class MinMax:
    def __init__(self):
        self.board = [0 for _ in range(9)]
        self.ai = 1
        self.player = 2
        self.tree = {}
        self.minmax(self.board.copy(), 1)
        self.minmax(self.board.copy(), 2)

    def win(self, v, board):
        for line in lines:
            if all([board[i] == v for i in line]):
                return True

        else:
            return False

    def score(self, board):
        if self.win(self.ai, board):
            return 10
        elif self.win(self.player, board):
            return -10
        else:
            return 0

    def to_str(self, board):
        s = ''
        for c in board:
            s += str(c)

        return s

    def minmax(self, board, mode):
        if self.score(board) != 0:
            return self.score(board)

        if 0 not in board:
            return 0

        scores = []
        steps = []
        for i in range(len(board)):
            if board[i] == 0:
                _board = board.copy()
                _board[i] = mode
                scores.append(self.minmax(_board, mode=abs(3 - mode)))
                steps.append(i)

        if mode == self.ai:
            self.tree[self.to_str(board)] = steps[np.argmax(scores)]
            return max(scores)
        else:
            return min(scores)

    def play(self, coord):

        if coord < -1 or coord >= 9:
            return 403

        if self.score(self.board) != 0:
            return 418

        if coord != -1 and self.board[coord] != 0:
            return 403

        if coord != -1:
            self.board[coord] = self.player

        move = self.tree.get(self.to_str(self.board), 418)
        if 0 <= move <= 8:
            self.board[move] = self.ai
        return move







