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
        self.easy_mode = None

    def menu(self):
        """
        menu
        :return:
        """
        menu = """
Which level do you want? Enter a number:
1 - simple operations with numbers 2-9
2 - integral squares of 11-29       
""".strip()

        while True:
            print(menu)
            choice: str = input()
            if choice == '1':
                self.easy_mode = True
                self.run(5)
                exit()
            elif choice == '2':
                self.easy_mode = False
                self.run(5)
                exit()
            else:
                print('Incorrect format.')

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

    def generate_example_hard(self):
        """
        get random numbers and operand
        """
        self.first_number = random.randint(11, 29)

    def print_example(self):
        """representation"""
        print(self.first_number, self.operand, self.second_number)

    def print_example_hard(self):
        """representation"""
        print(self.first_number)

    def print_answer(self):
        """representation"""
        print(self.evaluate_example())

    def test_example_easy(self):
        self.generate_example()
        self.print_example()

        while True:
            answer_text = input()

            try:
                answer = int(answer_text)

                if answer_text != str(self.evaluate_example()):
                    print('Wrong!')
                    return 0
                else:
                    print('Right!')
                    return 1

            except ValueError:
                print('Wrong format! Try again.')

    def test_example_hard(self):
        self.generate_example_hard()
        self.print_example_hard()

        while True:
            answer_text = input()

            try:
                answer = int(answer_text)

                if answer_text != str(self.evaluate_example_hard()):
                    print('Wrong!')
                    return 0
                else:
                    print('Right!')
                    return 1

            except ValueError:
                print('Wrong format! Try again.')

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

    def evaluate_example_hard(self) -> int:
        """

        :return: int
        """

        return self.first_number ** 2

    def run(self, n):
        """running full circle"""
        diff = {True: '1 - simple operations with numbers 2-9',
                False: '2 - integral squares 11-29'}

        result = 0
        for _ in range(n):
            if self.easy_mode:
                result += self.test_example_easy()
            else:
                result += self.test_example_hard()
        print(f'Your mark is {result}/{n}. Would you like to save your result to the file? Enter yes or no.')
        answer = input()
        if answer in ['yes', 'YES', 'y', 'Yes']:
            name = input('What is your name? ')
            with open("results.txt", "a") as f:
                f.write(f'{name}: {result}/5 in level {diff[self.easy_mode]}.\n')
                print('The results are saved in "results.txt".')


my_app = ArithmeticApp()
my_app.menu()
