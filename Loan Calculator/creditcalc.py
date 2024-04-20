import argparse
import math

def calc_months(loan, point, rate):
    n = math.ceil(math.log(point / (point - rate * loan), 1 + rate))
    years = n // 12
    message = 'It will take '

    if years == 1:
        message += f'{years} year'
    elif years > 0:
        message += f'{years} years'

    if (n - years * 12) > 0:
        message += ' and '

    if not (n - 12 * years):
        pass
    elif (n - 12 * years) == 1:
        message += f'{n - 12 * years} month'
    elif n > 0:
        message += f'{n - 12 * years} months'

    print(message + ' to repay this loan!')
    print(f'Overpayment = {int(point * n - loan)}')
def calc_loan(point, n, rate):
    loan = int(point / (rate * (1 + rate) ** n / ((1 + rate) ** n - 1)))
    print(f"Your loan principal = {loan}!")
    print(f'Overpayment = {int(point * n - loan)}')

def calc_monthly_payment(loan, n, rate):
    point = math.ceil(loan * rate * (1 + rate) ** n / ((1 + rate) ** n - 1))
    print(f"Your annuity payment = {point}")
    print(f'Overpayment = {point * n - loan}')
def calc_monthly_payment_diff(loan, n, rate):
    mpay = [0] * (n + 1)

    for i in range(1, n + 1):
        mpay[i] = math.ceil(loan / n + rate * (loan - loan * (i - 1)/n))
        print(f'Month {i}: payment is {mpay[i]}')
    print(f'\nOverpayment = {sum(mpay) - loan}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Moi moi')
    parser.add_argument("--payment")
    parser.add_argument("--principal")
    parser.add_argument("--periods")
    parser.add_argument("--interest")
    parser.add_argument("--type")

    args = parser.parse_args()
    # print(args)

    params = {'payment': args.payment,
              'principal': args.principal,
              'periods': args.periods,
              'interest': args.interest,
              'is_diff': args.type == 'diff',
              'is_ann': args.type == 'annuity',
              }
    if args.payment is not None and float(args.payment) < 0:
        print('Incorrect parameters')
    if args.principal is not None and float(args.principal) < 0:
        print('Incorrect parameters')
    if args.interest is not None and float(args.interest) < 0:
        print('Incorrect parameters')
    if args.periods is not None and int(args.periods) < 0:
        print('Incorrect parameters')

    _pn = 0
    if args.payment is None:
        _pn += 1
    if args.principal is None:
        _pn += 1
    if args.interest is None:
        _pn += 1
    if args.periods is None:
        _pn += 1

    match params:
        case {'is_diff': False, 'is_ann': False}:
            print('Incorrect parameters')
        case {'interest': None}:
            print('Incorrect parameters')
        case {'is_diff': True, 'payment': None}:
            calc_monthly_payment_diff(int(args.principal),
                                      int(args.periods),
                                      float(args.interest) / 12 / 100)

        case {'is_diff': True}:
            print('Incorrect parameters')
        case {'payment': None}:
            calc_monthly_payment(int(args.principal),
                                 int(args.periods),
                                 float(args.interest) / 12 / 100)
        case {'principal': None}:
            calc_loan(float(args.payment),
                      int(args.periods),
                      float(args.interest) / 12 / 100)
        case {'periods': None}:
            calc_months(int(args.principal),
                      float(args.payment),
                      float(args.interest) / 12 / 100)
        case _:
            print('Incorrect parameters')