"""
@author: Junxiao Song
"""
import numpy as np
# from policy_value_net import PolicyValueNet
from policy_value_net_numpy import PolicyValueNetNumpy
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
# import cPickle as pickle
import pickle


class Board:
    """
    board for the game
    """

    def __init__(self, width=8, height=8, n_in_row=5, start_player=0):
        self.width = width
        self.height = height
        self.n_in_row = n_in_row  # need how many pieces in a row to win

        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('Board width and height can not less than %d' % self.n_in_row)

        # board states, key:move as location on the board, value:player as pieces type
        self.states = {}

        self.players = [1, 2]  # player1 and player2
        self.current_player = self.players[start_player]  # start player
        self.availables = list(range(self.width * self.height))  # available moves
        self.last_move = -1

    def move_to_location(self, move):
        """
        3*3 board's moves like:
        6 7 8
        3 4 5
        0 1 2
        and move 5's location is (1,2)
        """
        h = move // self.width
        w = move % self.width

        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height):
            return -1

        return move

    def current_state(self):
        """return the board state from the perspective of the current player
        shape: 4*width*height"""

        square_state = np.zeros((4, self.width, self.height))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]
            square_state[0][move_curr // self.width, move_curr % self.height] = 1.0
            square_state[1][move_oppo // self.width, move_oppo % self.height] = 1.0

            # last move indication
            square_state[2][self.last_move // self.width, self.last_move % self.height] = 1.0

        if len(self.states) % 2 == 0:
            square_state[3][:, :] = 1.0

        return square_state[:, ::-1, :]

    def do_move(self, move):
        self.states[move] = self.current_player
        self.availables.remove(move)
        self.current_player = self.players[0] if self.current_player == self.players[1] else \
            self.players[1]
        self.last_move = move

    def has_a_winner(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row

        moved = list(set(range(width * height)) - set(self.availables))
        if len(moved) < self.n_in_row + 2:
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(
                        states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(
                        states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def game_end(self):
        """Check whether the game is ended or not"""
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.availables):  #
            return True, -1

        return False, -1

    def get_current_player(self):
        return self.current_player


def graphic(board, player1=1, player2=2):
    """
    Draw the board and show game info
    """
    width = board.width
    height = board.height

    print()
    print(player1, "with X".rjust(3))
    print(player2, "with O".rjust(3))
    print('  ', end='')
    for x in range(width):
        print("{0:4}".format(x), end='')
    print()
    for i in range(height - 1, -1, -1):
        print("{0:4d}".format(i), end='')
        for j in range(width):
            loc = i * width + j
            p = board.states.get(loc, -1)
            if p == player1:
                print('X'.center(4), end='')
            elif p == player2:
                print('O'.center(4), end='')
            else:
                print('_'.center(4), end='')
        print()


def state_arr(board, player1=1, player2=2):
    """
    Draw the board and show game info
    """
    width = board.width
    height = board.height

    state_str = ''

    for i in range(height - 1, -1, -1):
        for j in range(width):
            loc = i * width + j
            p = board.states.get(loc, -1)
            if p == player1:
                state_str += 'X'
            elif p == player2:
                state_str += 'O'
            else:
                state_str += '.'
        state_str += '\n'

    state_arr = [[_ for _ in row_str.strip()] for row_str in state_str.strip().split('\n')]

    return state_arr


class Game:
    def __init__(self, start_player=0):
        n = 5
        width, height = 8, 8
        model_file = 'AlphaZero_Gomoku/best_policy_8_8_5.model'

        if start_player not in (0, 1):
            raise Exception('start_player should be 0 (player1 first) or 1 (player2 first)')

        self.board = Board(width=width, height=height, n_in_row=n, start_player=start_player)

        # human VS AI
        # MCTS player with the policy_value_net trained by AlphaZero algorithm
        # policy_param = pickle.load(open(model_file, 'rb'))
        # best_policy = PolicyValueNet(width, height, net_params = policy_param)
        # mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # MCTS player with the trained policy_value_net written in pure numpy
        policy_param = pickle.load(open(model_file, 'rb'), encoding='bytes')  # To support python3
        best_policy = PolicyValueNetNumpy(width, height, policy_param)

        # set larger n_playout for better performance
        mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # uncomment the following line to play with pure MCTS
        # (its much weaker even with a larger n_playout)
        # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        p1, p2 = self.board.players

        self.bot = mcts_player

        # player1.set_player_ind(p1)
        # player2.set_player_ind(p2)

        self.players = {p1: 'bot', p2: 'human'}

        assert self.board.get_current_player() == 1  # bot is playing

        bot_move = self.bot.get_action(self.board)
        self.board.do_move(bot_move)

        # if is_shown:
        #     graphic(self.board, player1.player, player2.player)

    def is_move_valid(self, x, y):
        try:
            location = x, y
            human_move = self.board.location_to_move(location)
        except:
            human_move = -1

        if human_move == -1 or human_move not in self.board.availables:
            return False
        else:
            return True

    def state(self, player1=1, player2=2):
        width = self.board.width
        height = self.board.height

        state_str = ''

        for i in range(height - 1, -1, -1):
            for j in range(width):
                loc = i * width + j
                p = self.board.states.get(loc, -1)
                if p == player1:
                    state_str += 'X'
                elif p == player2:
                    state_str += 'O'
                else:
                    state_str += '.'
            state_str += '\n'

        state_arr = [[_ for _ in row_str.strip()] for row_str in state_str.strip().split('\n')]

        return state_arr

    def play(self, x, y, is_shown=False):

        """
        0 - continue
        1 - winner is bot
        2 - winner is human
        3 - tie
        4 - invalid move
        """

        assert self.board.get_current_player() == 2  # human is playing

        try:
            location = x, y
            human_move = self.board.location_to_move(location)
        except:
            human_move = -1

        if human_move == -1 or human_move not in self.board.availables:
            # print("Invalid move")
            return self.state(), 4

        self.board.do_move(human_move)

        if is_shown:
            graphic(self.board)

        end, winner = self.board.game_end()
        if end:
            if is_shown:
                if winner != -1:
                    print("Game end. Winner is ", self.players[winner])
                else:
                    print("Game end. Tie")
            return self.state(), winner

        assert self.board.get_current_player() == 1  # bot is playing

        bot_move = self.bot.get_action(self.board)
        self.board.do_move(bot_move)

        if is_shown:
            graphic(self.board)

        end, winner = self.board.game_end()
        if end:
            if is_shown:
                if winner != -1:
                    print("Game end. Winner is", self.players[winner])
                else:
                    print("Game end. Tie")
            return self.state(), winner

        return self.state(), 0


def test():
    game = Game()
    game.play(0, 0)
    game.play(0, 1)
    game.play(0, 2)
    game.play(0, 3)
    game.play(0, 5)


if __name__ == '__main__':
    test()
