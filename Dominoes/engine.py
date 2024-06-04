""" Module for Engine class """

import random

from field import Field


class Engine:
    """ A class representing the game engine for a dominos game"""

    def __init__(self, field: Field) -> None:
        """ Initialize a new game engine with given playing field. """

        self.field = field
        self.finished = False

    def play(self) -> None:
        """ Run game process until it's finished. """

        while not self.finished:
            self.report()
            self.make_move()
            self.switch_player()
            self.finished = self.check_game_over()
        self.report()

    def make_move(self):
        """ Make a move for the current player. """

        current_player = self.field.players[self.field.status]
        if current_player.is_computer():
            input()
            move = self.random_move(current_player.size())
        else:
            move = self.get_move(current_player.size())
        self.transfer(move)

    def transfer(self, m: int) -> None:

        player = self.field.players[self.field.status]
        if m > 0:  # add a domino to the right end of the snake
            self.field.snake.add_domino(player.pop_domino(m - 1))
        elif m < 0:  # add a domino to the left end of the snake
            self.field.snake.add_domino(player.pop_domino(abs(m) - 1), left=True)
        elif self.field.stock.size():
            player.add_domino(self.field.stock.pop_domino())

    @staticmethod
    def get_move(size) -> int:
        """ Make a turn as a player """

        while True:
            try:
                move = int(input())
                if not -size <= move <= size:
                    raise ValueError
            except ValueError:
                print('Invalid input. Please try again.')
                continue
            else:
                return move


    def check_game_over(self) -> bool:
        """ Check if the game is finished """

        for player in self.field.players:
            if player.size() == 0:
                return True

        snake = self.field.snake

        if snake.size():
            left = snake.dominos[0].a
            right = snake.dominos[-1].b
            return sum((domino.a == left) + (domino.b == right) for domino in snake.dominos) == 8

        return False

    @staticmethod
    def random_move(n):
        return random.choice(range(-n, n + 1))

    def switch_player(self) -> None:
        """ Switch to the next player. """

        self.field.status = (self.field.status + 1) % len(self.field.players)

    def report(self):
        """ Report the current state of the game. """

        computer = self.field.players[0]
        player = self.field.players[1]
        stock_size = self.field.stock.size()
        computer_size = computer.size()
        player_size = player.size()
        game_status = self.field.status

        print(f'{"=" * 70}\n'
              f'Stock size: {stock_size}\n'
              f'Computer pieces: {computer_size}\n'
              f'{self.field}\n'
              f'Your pieces:\n'
              f'{player}')

        status = 'Status: '
        if self.finished:
            result = ('You won!' if player_size == 0 else
                      'The computer won!' if computer_size == 0 else
                      "It's a draw!")
            status += f'The game is over. {result}'
        else:
            status += ('Computer is about to make a move. Press Enter to continue...' if game_status == 0 else
                       "It's your turn to make a move. Enter your command." if game_status == 1 else
                       'Invalid game status')
        print(status)
