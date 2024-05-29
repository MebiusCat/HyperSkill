import random


class Player:
    def __init__(self, name, ai=False):
        self.name = name
        self.domino = []
        self.ai = ai

    def __str__(self):
        # return f'{self.name} pieces: [{", ".join(str(domino) for domino in self.domino)}]'
        return '\n'.join(f"{k + 1}:{str(domino)}" for k, domino in enumerate(self.domino))

    def __len__(self):
        return len(self.domino)

    def add_domino(self, x):
        self.domino.append(x)

    def pop_domino(self, idx):
        return self.domino.pop(idx)

    def largest_double(self):
        largest = None
        for domino in self.domino:
            if domino.is_double():
                if not largest or largest.a < domino.a:
                    largest = domino
        return largest

    def find_domino(self, x):
        for k, elem in enumerate(self.domino):
            if elem == x:
                return k

    def turn_is_valid(self, pos):
        try:
            return pos and abs(int(pos)) < len(self) + 1
        except ValueError:
            return False


    def turn_ai(self):
        place = input()
        place = random.choice(range(-len(self), len(self)))
        return place < 0, None if not place else self.pop_domino(abs(place) - 1)

    def turn_player(self):
        while not self.turn_is_valid(place := input()):
            print('Invalid input. Please try again.')
            continue
        place = int(place)
        return place < 0, None if not place else self.pop_domino(abs(place) - 1)

    def turn(self):
        return self.turn_ai() if self.ai else self.turn_player()
