class Stock:
    def __init__(self):
        self.name = 'Stock'
        self.domino = []

    def __str__(self):
        return f'Stock pieces: [{", ".join(str(domino) for domino in self.domino)}]'

    def add_domino(self, x):
        self.domino.append(x)

    def pop_domino(self, idx):
        return self.domino.pop(idx)

    def __len__(self):
        return len(self.domino)
