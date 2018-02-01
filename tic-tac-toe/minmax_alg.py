import re

import numpy as np

lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
opponent = lambda x: 'x' if x == 'o' else 'o'


def around2(board, i, mode):
    s = 0
    for line in lines:
        if i in line:
            res = sum([board[j] == mode for j in line])
            if res == 2:
                s += 10
    return s


def potential_lines(board, i, mode):
    s = 0
    for line in lines:
        if i in line:
            s += 1
            if any(([board[j] == opponent(mode) for j in line])):
                s -= 1

    return s


class MinMax:
    def __init__(self):
        self.board = ['.' for _ in range(9)]
        self.ai = 'o'
        self.player = 'x'

    def win(self, v, board):
        for line in lines:
            if all([board[i] == v for i in line]):
                return True
        else:
            return False

    def score(self, board, player):
        if self.win(player, board):
            return 10
        elif self.win(opponent(player), board):
            return -10
        else:
            return 0

    def to_str(self, board):
        s = ''
        for c in board:
            s += str(c)

        return s

    def from_input(self, s):
        s = s.replace('\n', '')
        return list(s)

    @staticmethod
    def to_output(board):
        result = list(map(lambda x: x.replace('x', '❌').replace('o', '⭕️'), board))
        return [result[:3], result[3:6], result[6:]]

    def minmax(self, board, mode, player):
        wanted_sc = 10 if mode == player else -10

        if '.' not in board:
            return 0, -1

        if self.is_empty(board):
            return 0, 4

        scores = []
        steps = []
        free = [i for i in range(len(board)) if board[i] == '.']
        rates = [0 for _ in range(len(free))]
        for curr in range(len(free)):
            rates[curr] += around2(board, free[curr], mode)
            rates[curr] += 3 * around2(board, free[curr], opponent(mode))
            rates[curr] += potential_lines(board, free[curr], mode)

        while free:
            arg = np.argmax(rates)
            move = free[arg]
            free.pop(arg)
            rates.pop(arg)

            _board = board.copy()
            _board[move] = mode
            if self.score(_board, player) == wanted_sc:
                return wanted_sc, move

            sc, step = self.minmax(_board, mode=opponent(mode), player=player)
            if sc == wanted_sc:
                return wanted_sc, move

            scores.append(sc)
            steps.append(move)

        else:
            if mode == player:
                step = steps[np.argmax(scores)]
                return max(scores), step
            else:
                return min(scores), -1

    def is_empty(self, board):
        return all([x == '.' for x in board])

    def play(self, s):

        if not self.board_valid(s):
            return '', 403

        board = self.from_input(s)

        if self.is_empty(board):
            self.player, self.ai = 'o', 'x'

        if self.score(board, self.ai) != 0:
            return self.to_output(board), 418

        s, move = self.minmax(board, self.ai, self.ai)
        if 0 <= move <= 8:
            board[move] = self.ai
            self.board = board
            return self.to_output(board), 200 if self.score(board, self.ai) == 0 else 418

        else:
            return self.to_output(board), 418

    def play2(self, move):

        if move == -1:
            self.player, self.ai = 'o', 'x'

        elif 0 <= move <= 8:
            self.board[move] = self.player

        # if game over after player's movement
        if self.score(self.board, self.ai) != 0:
            return self.to_output(self.board), 2

        if '.' not in self.board:
            return self.to_output(self.board), 3

        # ai movement
        s, ai_move = self.minmax(self.board, self.ai, self.ai)
        if 0 <= ai_move <= 8:
            self.board[ai_move] = self.ai

        # if game over after ai's movement
        if self.score(self.board, self.ai) != 0:
            return self.to_output(self.board), 1

        elif '.' not in self.board:
            return self.to_output(self.board), 3

        else:
            return self.to_output(self.board), 0

    def valid(self, move):
        if self.is_empty(self.board) and move == -1:
            return True

        if move not in range(0, 9):
            return False

        elif self.board[move] != '.':
            return False

        elif self.score(self.board, self.ai) != 0:
            return False

        return True

    def board_valid(self, board):
        pattern = re.compile("[xo\.]{3}\n[xo\.]{3}\n[xo\.]{3}")

        legal_change = 0
        new_b = self.from_input(board)
        for i in range(len(new_b)):
            if new_b[i] == self.board[i]:
                continue

            elif new_b[i] == self.player and self.board[i] == '.':
                legal_change += 1

            else:
                print('does not match')
                return False

        else:
            if legal_change not in [0, 1]:
                print('not legal move')
                return False

        return pattern.fullmatch(board) is not None
