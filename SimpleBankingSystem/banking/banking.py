import sqlite3
from random import sample


class BankingSystem:

    def __init__(self):
        self.card_data = None
#        self.cards: dict = dict()
        self.database()

    def menu(self) -> None:
        while True:
            print('1. Create an account\n2. Log into account\n0. Exit')
            choise = input('>')
            if choise == '1':
                self.create_account()
            elif choise == '2':
                self.login()
            elif choise == '0':
                print('Bye')
                exit()
            else:
                print('Unknown option!')

    def account(self) -> None:

        while True:
            print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
            choise = input('>')
            if choise == '1':
                print(f'\nBalance: {self.card_data[2]}\n')
#                print(f"Balance: {self.cards[card]['Balance']}\n")
            elif choise == '2':
                self.add_income(self.card_data[0], self.card_data[2])
                self.card_data = self.check_credentials(self.card_data[0])
            elif choise == '3':
                self.transfer(self.card_data[0], self.card_data[2])
                self.card_data = self.check_credentials(self.card_data[0])
            elif choise == '4':
                self.delete_account(self.card_data[0])
                self.card_data = None
                self.menu()
            elif choise == '5':
                self.card_data = None
                print('You have successfully logged out!\n')
                return
            elif choise == '0':
                print('Bye')
                exit()
            else:
                print('Unknown option!')

    @staticmethod
    def database(card=None, pin=None, balance=None) -> None:
        with sqlite3.connect('card.s3db') as data:
            cursor = data.cursor()
            if not card:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS card(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL UNIQUE,
                pin TEXT NOT NULL,
                balance INTEGER DEFAULT 0 NOT NULL
                );
                ''')
            else:
                print('new create')
                cursor.execute('''
                INSERT OR IGNORE INTO card (number, pin, balance)
                VALUES (?, ?, ?);
                ''', (card, pin, balance))

    @staticmethod
    def check_credentials(card) -> tuple:
        with sqlite3.connect('card.s3db') as data:
            cursor = data.cursor()
            cursor.execute('''
            SELECT number, pin, balance FROM card WHERE number LIKE (?);
            ''', (card, ))
            return cursor.fetchone()

    @staticmethod
    def add_income(card, balance) -> None:
        income = int(input("Enter income:\n>"))
        with sqlite3.connect('card.s3db') as data:
            cursor = data.cursor()
            cursor.execute('''
            UPDATE card
            SET balance = (?)
            WHERE number LIKE (?);
            ''', (balance + income, card, ))

            print('Income was added!\n')

    @staticmethod
    def delete_account(card) -> None:
        with sqlite3.connect('card.s3db') as data:
            cursor = data.cursor()
            cursor.execute('''
            DELETE FROM card
            WHERE number LIKE (?);
            ''', (card, ))

            print('The account has been closed!\n')

    @staticmethod
    def transfer(card, balance) -> None:
        transfer_number = input("Enter card number:\n>")

        if str(BankingSystem.luhn_algorithm(transfer_number[:-1])) != transfer_number[-1]:
            print('Probably you made mistake in the card number. Please try again!\n')
            return

        if transfer_number == card:
            print("You can't transfer money to the same account!")

        transfer_card = BankingSystem.check_credentials(transfer_number)

        if not transfer_card:
            print('Such a card does not exist\n')

        else:
            transfer_sum = int(input('Enter how much money you want to transfer:\n'))

            if balance < transfer_sum:
                print('Not enough money!\n')
                return

            with sqlite3.connect('card.s3db') as data:
                cursor = data.cursor()
                cursor.execute('''
                UPDATE card
                SET balance = (?)
                WHERE number LIKE (?);
                ''', (balance - transfer_sum, card, ))

                cursor.execute('''
                UPDATE card
                SET balance = (?)
                WHERE number LIKE (?);
                ''', (transfer_card[2] + transfer_sum, transfer_card[0],))
                print('Success!\n')
            data.commit()
    # @staticmethod
    def generate_account(self) -> tuple:
        while True:
            card = '400000' + ''.join([str(n) for n in sample(range(10), 9)])
            card += str(self.luhn_algorithm(card))
            PIN = ''.join([str(n) for n in sample(range(10), 4)])
            if not BankingSystem.check_credentials(card):
                yield card, PIN
            else:
                continue

    @staticmethod
    def luhn_algorithm(card) -> int:
        double = card[::2]
        double_int = [int(x) * 2 for x in double]
        double_int = [x if x < 9 else x - 9 for x in double_int]
        total = sum(double_int) + sum([int(x) for x in card[1::2]])
        total %= 10
        return 10 - total if total else 0

    def create_account(self) -> None:
        card, PIN = next(self.generate_account())
        self.database(card, PIN, 0)

        print("\nYour card has been created")
        print(f"Your card number:\n{card}")
        print(f"Your card PIN:\n{PIN}\n")

    def login(self) -> None:
        card = input("Enter your card number:\n>")
        PIN = input("Enter your PIN:\n>")
        try:
            self.card_data = self.check_credentials(card)
            if self.card_data[1] == PIN:
                print('You have successfully logged in!\n')
                self.account()
            else:
                print('Wrong card number or PIN\n')
        except (KeyError, TypeError):
            print('Wrong card number or PIN\n')
        '''     
        try:           
            if self.cards[card]['PIN'] == PIN:
                print("You have successfully logged in!\n")
                self.account(card)
            else:
                print("Wrong card number or PIN!\n")
        except KeyError:
            print("Wrong card number or PIN!\n")
        '''

#


#with sqlite3.connect('card.s3db') as data:
#    cursor = data.cursor()
#    cursor.execute('''
#    SELECT number, pin, balance FROM card ;
#    ''')
#    print(cursor.fetchall())

BankingSystem().menu()
