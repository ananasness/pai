class Matches:
    def __init__(self):
        self.state = 21

    def play(self, state):
        # Bot loose condition
        if state == 1:
            return 1
        # Bot win condition
        if state == 0:
            return 2

        lose_states = [1 + 4 * x for x in range(6) if 1 + 4 * x <= state]

        if state in lose_states:
            self.state -= 1
        else:
            self.state = lose_states[-1]

        return 0

    def state_valid(self, state):
        return 1 <= self.state - state <= 3 \
               and 0 <= state <= 21
