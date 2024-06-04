import random
from itertools import combinations_with_replacement

from domino import Domino
from player import Player
from stock import Stock


class Field:
    def __init__(self):
        self.name = "Domino snake"
        self.snake = Stock()
        self.status = None
        self.players: list(Player) = []
        self.stock = Stock()

    def __str__(self):
        s = self.snake.dominos
        return ''.join(map(str, s[:3] + ['...'] + s[-3:]) if len(s) >= 7 else ''.join(map(str, s)))

    def generate(self, player_names):
        while True:
            dominoes = [Domino(a, b) for a, b in combinations_with_replacement(range(7), 2)]
            random.shuffle(dominoes)

            self.stock = Stock()
            for _ in range(14):
                self.stock.add_domino(dominoes.pop())

            self.players = [Player(name, npc) for name, npc in player_names]

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
                self.snake.add_domino(largest)
                self.players[self.status].pop_domino(self.players[self.status].find_domino(largest))
                self.status = (self.status + 1) % len(self.players)
                break
