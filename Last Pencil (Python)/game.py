import random

class Pencil:
    def __init__(self):
        self.player_1 = 'John'
        self.player_2 = 'Jack'
        self.size: int = self._set_pencils()
        self.turn = {'John': self.player_play, 'Jack': self.bot}
        self.side = {True: self.player_1, False: self.player_2}
        self.human_start = True

        player_str = 'Who will be the first (John, Jack): '
        self.player = input(player_str)

        while self.player not in [self.player_1, self.player_2]:
            print(f'Choose between {self.player_1} and {self.player_2}')
            self.player = input()

        if self.player == self.player_2:
            self.human_start = False

    def _set_pencils(self) -> int:
        pencils: str = input('How many pencils would you like to use: ')

        while not pencils.isnumeric() and (int(pencils) > 0):
            if int(pencils) == 0:
                print('The number of pencils should be positive')
            elif int(pencils) < 0:
                print('The number of pencils should be numeric (the minus sign is not a numeric)')
            else:
                print('The number of pencils should be numeric')
            pencils = input()

        return int(pencils)

    def play(self):
        player_turn = self.human_start

        while self.size > 0:
            print(self.size * '|')
            print(f"{self.side[player_turn]}'s turn:")

            amount = self.turn[self.side[player_turn]]()
            player_turn = not player_turn
            self.size -= amount

            if self.size == 0:
                print(f"{self.side[player_turn]} won!")

    def bot(self):
        if self.size == 1:
            print('1')
            return 1

        decision = {0: 3, 2: 1, 3: 2}

        appendix = self.size % 4

        if appendix == 1:
            amount = random.randint(1, 3)
        else:
            amount = decision[appendix]
        print(amount)
        return amount

    def player_play(self):
        while True:
            try:
                amount = int(input())
                if amount not in [1, 2, 3]:
                    print("Possible values: '1', '2' or '3'")
                elif amount > self.size:
                    print("Too many pencils")
                else:
                    return amount
            except ValueError:
                print("Possible values: '1', '2' or '3'")


p_game = Pencil()
p_game.play()