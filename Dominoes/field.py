import random
from itertools import combinations_with_replacement

from domino import Domino
from player import Player
from stock import Stock


class Field:
    def __init__(self):
        self.name = "Domino snake"
        self.snake = []
        self.status = None
        self.players = []
        self.stock = None

    def __str__(self):
        return f'{self.name} [{", ".join(str(domino) for domino in self.snake)}]'

    def add_domino(self, x):
        self.stock.append(x)

    def next_player(self):
        print(f'Status: {self.players[(self.status + 1) % len(self.players)].name.lower()}')

    def generate(self, player_names):
        while True:
            dominoes = [Domino(a, b) for a, b in combinations_with_replacement(range(7), 2)]
            random.shuffle(dominoes)

            self.stock = Stock()
            for _ in range(14):
                self.stock.add_domino(dominoes.pop())

            self.players = [Player(name) for name in player_names]

            for _ in range(7):
                for pld in self.players:
                    pld.add_domino(dominoes.pop())

            largest = None
            for idx, pld in enumerate(self.players):
                dom = pld.largest_double()
                if Domino.larger_double(largest, dom) > 0:
                    largest = dom
                    self.status = idx

            if largest:
                self.snake.append(largest)
                self.players[self.status].pop_domino(self.players[self.status].find_domino(largest))
                break
