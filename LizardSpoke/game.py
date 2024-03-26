import random


class TickTackToe:

    def __init__(self):
        self.winChoice = {'rock': 'paper',
                          'scissors': 'rock',
                          'paper': 'scissors'}

        self.var = ['rock', 'paper', 'scissors']
        self.rating_list = {}
        self.middle = 1

        with open('rating.txt', 'r') as f:
            for a in f:
                name, rating = a.split(" ")
                self.rating_list[name] = int(rating)

    def play(self):
        name = input('Enter your name: ')
        print(f'Hello, {name}')

        alternative_list = input()
        if len(alternative_list) > 0:
            self.var = alternative_list.split(',')
            self.middle = (len(self.var) - 1) // 2

        if name not in self.rating_list:
            self.rating_list[name] = 0

        print("Okay, let's start")

        while True:
            user_choice = input()

            if user_choice == '!exit':
                print('Bye!')
                break
            elif user_choice == '!rating':
                curr_rating = 0
                if name in self.rating_list:
                    curr_rating = self.rating_list[name]
                print(f'Your rating: {curr_rating}')
                continue

            if user_choice not in self.var:
                print('Invalid input')
            else:
                self.epoh(user_choice, name)

    def epoh(self, user_choice, name):

        ai_choice = random.choice(self.var)
        ai_index = self.var.index(ai_choice)
        new_var = self.var[ai_index:] + self.var[:ai_index]

        if user_choice == ai_choice:
            print(f'There is a draw ({user_choice})')
            self.rating_list[name] += 50
        elif user_choice not in new_var[self.middle + 1:]:
            print(f'Well done. The computer chose {ai_choice} and failed')
            self.rating_list[name] += 100
        else:
            print(f'Sorry, but the computer chose {ai_choice}')


game = TickTackToe()
game.play()
