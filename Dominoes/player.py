class Player:
    def __init__(self, name):
        self.name = name
        self.domino = []

    def __str__(self):
        return f'{self.name} pieces: [{", ".join(str(domino) for domino in self.domino)}]'

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
