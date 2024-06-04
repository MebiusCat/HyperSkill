""" Stock class"""

from domino import Domino


class Stock:
    def __init__(self) -> None:
        self.dominos: list[Domino] = []

    def __str__(self):
        return f'Stock pieces: [{", ".join(str(domino) for domino in self.dominos)}]'

    def add_domino(self, x, left=False):
        """ Add a domino to the stock. If left is True, add it to the left. Otherwise, add it to the right. """

        if left:
            self.dominos.insert(0, x)
        else:
            self.dominos.append(x)

    def pop_domino(self):
        """ Remove a domino from stock """

        return self.dominos and self.dominos.pop()

    def size(self) -> int:
        """ Return the size of the stock. """

        return len(self.dominos)
