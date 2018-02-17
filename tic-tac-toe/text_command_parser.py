import random
from nltk.metrics import *
from nltk import word_tokenize


def command_parse(s):
    games = ['tictactoe', 'matches', 'equation', 'fiveinarow', 'randomgame']
    symbols = """!@#$%^&*()_+-=[]{}:"'\|?/>.<,`~"""
    tokens = [token.strip(symbols).lower() for token in word_tokenize(s)]
    phones = ''.join(tokens)

    min_dist = 4
    winner = None
    for i in range(len(phones)):
        for j, g in enumerate(games):
            if i + len(g) < len(phones):
                dist = edit_distance(g, phones[i:i + len(g) + 1])
                if dist <= min_dist:
                    min_dist = dist
                    winner = games[j]

    if winner == 'randomgame':
        return random.choice(games[:-1])
    else:
        return winner
