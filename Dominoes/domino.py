class Domino:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return f"[{self.a}, {self.b}]"

    def is_double(self):
        return self.a == self.b

    @staticmethod
    def larger_double(x, y):
        if y is None:
            return 0
        if x is None:
            return 1

        return y.a - x.a
