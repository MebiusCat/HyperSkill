# bill spliiter

import random

NUM_STR = 'Enter the number of friends joining (including you):\n'
GUEST_STR = 'Enter the name of every friend (including you), each on a new line:'
BILL_STR = 'Enter the total bill value:\n'
LUCKY_STR = 'Do you want to use the "Who is lucky?" feature? Write Yes/No:\n'
NO_LUCKY_STR = 'No one is going to be lucky'

def number_is_correct(num):
    return num > 0

def party():
    n = int(input(NUM_STR))

    if not number_is_correct(n):
        print("No one is joining for the party\n")
        return

    print(GUEST_STR)
    _members = [input() for _ in range(n)]

    bill_amount = int(input(BILL_STR))
    part = round(bill_amount / n, 2)

    members = dict.fromkeys(_members, part)
    get_lucky = input(LUCKY_STR)
    if get_lucky == 'Yes':
        lucky_person = random.choice(_members)
        print(f'{lucky_person} is the lucky one!')

        part = round(bill_amount / (n - 1), 2)
        for k in members:
            members[k] = 0 if k == lucky_person else part
    else:
        print('No one is going to be lucky')
    print(members)

party()