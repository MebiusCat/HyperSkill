from domino import Domino

import random


class Player:
    def __init__(self, name, ai) -> None:
        self.name = name
        self.dominos: list[Domino] = []
        self.ai = ai

    def __str__(self):
        # return f'{self.name} pieces: [{", ".join(str(domino) for domino in self.domino)}]'
        return '\n'.join(f"{k + 1}:{str(domino)}" for k, domino in enumerate(self.dominos))

    def __len__(self):
        return len(self.dominos)

    def add_domino(self, x):
        self.dominos.append(x)

    def pop_domino(self, idx):
        return self.dominos.pop(idx)

    def largest_double(self):
        largest = None
        for domino in self.dominos:
            if domino.is_double():
                if not largest or largest.a < domino.a:
                    largest = domino
        return largest

    def find_domino(self, x):
        for k, elem in enumerate(self.dominos):
            if elem == x:
                return k

    def size(self):
        """ Return the size of the player's stack. """

        return len(self.dominos)

    def is_computer(self):
        return self.ai