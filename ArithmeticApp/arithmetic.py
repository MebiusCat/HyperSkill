"""simple arithmetic operations"""

import random as random


class ArithmeticApp:
    """my class"""
    def __init__(self):
        """init """
        self.first_number = None
        self.second_number = None
        self.operand = None
        self.pool = ['+', '-', '*']

    def read_example(self):
        """
        insert example manually
        """
        text = input()
        fn_text, operand, sn_text = text.split(' ')
        self.first_number = int(fn_text)
        self.second_number = int(sn_text)

    def generate_example(self):
        """
        get random numbers and operand
        """
        self.first_number = random.randint(2, 9)
        self.second_number = random.randint(2, 9)
        self.operand = random.choice(self.pool)

    def print_example(self):
        print(self.first_number, self.operand, self.second_number)

    def print_answer(self):
        print(self.evaluate_example())

    def test_example(self):
        self.generate_example()
        self.print_example()
        answer = input()
        if answer != str(self.evaluate_example()):
            print('Wrong!')
        else:
            print('Right!')

    def evaluate_example(self) -> int:
        """

        :return: int
        """
        if self.operand == '+':
            return self.first_number + self.second_number
        elif self.operand == '-':
            return self.first_number - self.second_number
        elif self.operand == '*':
            return self.first_number * self.second_number


my_app = ArithmeticApp()
my_app.test_example()
