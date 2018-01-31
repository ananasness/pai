class Matches:

    def __init__(self):
        self.state = 21

    def play(self, state):
        if not self.state_valid(state):
            return 0, 403

        if state in [0, 13]:
            return 0, 418

        lose_states = [1 + 4*x for x in range(6) if 1 + 4*x <= state]

        if state in lose_states:
            self.state -= 1

        else:
            self.state = lose_states[-1]

        return self.state, 200

    def state_valid(self, state):
        return self.state - state in [1, 2, 3] \
               and 0 <= state <= 21
