""" We've just opened! """

from recipes import Recipe

BEAN_STR = 'Write how many grams of coffee beans the coffee machine has:'
WATER_STR = 'Write how many ml of water the coffee machine has:'
MILK_STR = 'Write how many ml of milk the coffee machine has:'
CUPS_STR = 'Write how many disposable cups you want to add:'


class CoffeeMaker:

    def __init__(self):

        self.recipes: list[Recipe] = []

        self.bean_stock = 120
        self.water_stock = 400
        self.milk_stock = 540
        self.cups_stock = 9
        self.money = 550

    def menu(self):

        while True:
            choice = input(f'Write action (buy, fill, take):\n')
            if choice == 'buy':
                self.make_a_coffee()
            elif choice == 'fill':
                self.stock_up()
            elif choice == 'take':
                self.encashment()
            elif choice == 'remaining':
                self.machine_status()
            else:
                break


    def encashment(self):
        print(f'I gave you ${self.money}\n')
        self.money = 0

    def make_a_coffee(self):
        menu = 'What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:'

        position = input(menu)

        if position == 'back':
            return

        position = int(position)

        if position not in range(len(self.recipes) + 1):
            print("Wrong coffee type")
            return

        cur_coffee = self.recipes[position - 1]

        if self.check_supply(
                cur_coffee.water, cur_coffee.milk, cur_coffee.beans, 1):
            print('I have enough resources, making you a coffee!')
            self.water_stock -= cur_coffee.water
            self.milk_stock -= cur_coffee.milk
            self.bean_stock -= cur_coffee.beans
            self.cups_stock -= 1
            self.money += cur_coffee.price

    def machine_status(self):
        print(f'The coffee machine has:\n'
              f'{self.water_stock} ml of water\n'
              f'{self.milk_stock} ml of milk\n'
              f'{self.bean_stock} g of coffee beans\n'
              f'{self.cups_stock} disposable cups\n'
              f'${self.money} of money\n')

    def load_recipes(self):
        self.recipes = [
            Recipe('espresso', 250, 0, 16, 4),
            Recipe('latte', 350, 75, 20, 7),
            Recipe('cappuccino', 200, 100, 12, 6)
        ]

    def stock_up(self):

        self.water_stock += int(input(WATER_STR))
        self.milk_stock += int(input(MILK_STR))
        self.bean_stock += int(input(BEAN_STR))
        self.cups_stock += int(input(CUPS_STR))

    @staticmethod
    def order_planning(water, milk, bean):

        cups = int(input('Write how many cups of coffee you will need:\n'))
        print(f'For {cups} cups of coffee you will need:'
              f'{cups * water} ml of water'
              f'{cups * milk} ml of milk'
              f'{cups * bean} g of coffee beans')

    def check_supply(self, water, milk, beans, cups):

        out_of = []

        if self.water_stock < water * cups:
            out_of.append('water')

        if self.milk_stock < milk * cups:
            out_of.append('milk')

        if self.bean_stock < beans * cups:
            out_of.append('coffee beans')

        if out_of:
            print('Sorry, not enough', ','.join(w for w in out_of), '!')

        return len(out_of) == 0


    def order_reservation(self, water, milk, bean):

        cups = int(input('Write how many cups of coffee you will need:\n'))
        n_portions = min(self.water_stock // water,
                         self.bean_stock // bean,
                         self.milk_stock // milk)

        if cups == n_portions:
            print('Yes, I can make that amount of coffee')
        elif cups > n_portions:
            print(f'No, I can make only {n_portions} cups of coffee')
        else:
            print(f'Yes, I can make that amount of coffee (and even {n_portions - cups} more than that)')

    @staticmethod
    def starter():
        print('Starting to make a coffee',
              'Grinding coffee beans',
              'Boiling water',
              'Mixing boiled water with crushed coffee beans',
              'Pouring coffee into the cup',
              'Pouring some milk into the cup',
              'Coffee is ready!', sep='\n')


if __name__ == "__main__":
    barista = CoffeeMaker()
    barista.load_recipes()
    barista.menu()
