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
        # return f'{self.name} [{", ".join(str(domino) for domino in self.snake)}]'
        if len(self.snake) < 7:
            return f'{" ".join(str(domino) for domino in self.snake)}'

        return (f'{" ".join(str(domino) for domino in self.snake[:3])}'
                + '...'
                + f'{" ".join(str(domino) for domino in self.snake[-3:])}')


    def make_turn(self):
        player = (self.status + 1) % len(self.players)
        left, domino = self.players[player].turn()
        if domino is None:
            self.players[player].add_domino(self.stock.pop_domino(0))
        else:
            if left:
                self.snake.insert(0, domino)
            else:
                self.snake.append(domino)
        self.status = player
        # print(self)

    def is_finished(self):
        for player in self.players:
            if not len(player):
                if player.ai:
                    self.display_ending()
                    print('Status: The game is over. The computer won!')
                else:
                    self.display_ending()
                    print('Status: The game is over. You won!')
                return True
        fish_counter = {i: 0 for i in range(7)}
        for domino in self.snake:
            fish_counter[domino.a] += 1
            fish_counter[domino.b] += 1
            if fish_counter[domino.a] == 8 or fish_counter[domino.b] == 8:
                self.display_ending()
                print("Status: The game is over. It's a draw!")
                return True
        return False

    def run_game(self):
        while not self.is_finished():
            self.display_header()
            self.make_turn()

    def display_header(self):
        print("=" * 70)
        print(f"Stock size: {len(self.stock)}")

        player = self.players[1]
        computer = self.players[0]

        print(f"Computer pieces: {len(computer)}")
        # print(f"\n{', '.join(str(domino) for domino in self.snake)}\n")
        print(f"\n{self}\n")
        print("Your pieces:")
        print(player)
        if self.status:
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        else:
            print("\nStatus: It's your turn to make a move. Enter your command.")


    def display_ending(self):
        print("=" * 70)
        print(f"Stock size: {len(self.stock)}")

        player = self.players[1]
        computer = self.players[0]

        print(f"Computer pieces: {len(computer)}")
        print(f"\n{self}\n")
        print("Your pieces:")
        print(player)

    def next_player(self):
        print(f'Status: {self.players[(self.status + 1) % len(self.players)].name.lower()}')

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
                self.snake.append(largest)
                self.players[self.status].pop_domino(self.players[self.status].find_domino(largest))
                break
