import requests
import json

def update_rates(cur, dict_rates, base=['usd', 'eur']):
    r = requests.get(f'http://www.floatrates.com/daily/{cur.lower()}.json')
    response = json.loads(r.text)
    for elem in base:
        if cur not in dict_rates:
            dict_rates[cur] = {}
        if not cur == elem:
            dict_rates[cur][elem] = response[elem]

currency_rates = {}

currency = input()
update_rates(currency, currency_rates)

while (exchange_cur:= input()):
    amount = float(input())

    print('Checking the cache...')
    if exchange_cur not in currency_rates[currency]:
        print('Sorry, but it is not in the cache!')
        update_rates(currency, currency_rates, [exchange_cur])
    else:
        print('Oh! It is in the cache!')
    rate = currency_rates[currency][exchange_cur]['rate']
    print(f'You received {round(rate * amount, 2)} {exchange_cur}.')

print("This is the END")

# Stage 5
# currency = input()
#
# r = requests.get(f'http://www.floatrates.com/daily/{currency.lower()}.json')
# response = json.loads(r.text)
# print(response['usd'], response['eur'], sep='\n')


# Stage 1-4
# currency = {'RUB': 2.98, 'ARS': 0.82, 'HNL': 0.17,
#             'AUD': 1.9622, 'MAD': 0.208}
#
# in_purse = float(input())
# for cur, rate in currency.items():
#     print(f'I will get {in_purse * rate} {cur} from the sale of {in_purse} conicoins.')
