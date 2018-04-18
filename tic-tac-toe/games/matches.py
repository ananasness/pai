class Matches:
    def __init__(self):
        self.state = 21

    def play(self, state):
        move = 0
        # Bot loose condition
        if state == 1:
            return move, 1
        # Bot win condition
        if state == 0:
            return move, 2

        lose_states = [1 + 4 * x for x in range(6) if 1 + 4 * x <= state]

        if state in lose_states:
            self.state -= 1
            move = 1
        else:
            move = state - lose_states[-1]
            self.state = lose_states[-1]

        return move, 0

    def state_valid(self, state):
        return 1 <= self.state - state <= 3 \
               and 0 <= state <= 21
