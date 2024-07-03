"""Compose a binary string"""

CHAR_LIMIT = 100

from random import choice

def char_validation(char):
    if char not in '01':
        return ''
    return char


def update_text(_text, _input):
    for char in _input:
        if char_validation(char):
            _text += char
    return _text


def text_validation(_text):
    count_symbols = len(_text)

    if count_symbols < CHAR_LIMIT:
        print(f'Current data length is {count_symbols}, {CHAR_LIMIT - count_symbols} symbols left')

    return len(_text) >= CHAR_LIMIT


def count_triplets(data):

    triads = dict()

    for i in range(len(data) - 3):
        triplet, follow = data[i: i + 3], data[i + 3]
        if triplet not in triads:
            triads[triplet] = dict.fromkeys(['0', '1'], 0)
        triads[triplet][follow] += 1
    return triads


def predict(triplet, frequency):
    if triplet not in frequency:
        return choice(['0', '1'])
    left, right = frequency[triplet].items()
    if left[1] == right[1]:
        return choice(['0', '1'])
    elif left[1] > right[1]:
        return left[0]
    else:
        return right[0]


def make_prediction(sample, frequency):
    res = ''
    for i in range(len(sample) - 3):
        res += predict(sample[i: i + 3], frequency)
    return res


def accuracy(sample, prediction):
    acc = [prediction[i] == sample[i + 3] for i in range(len(prediction))]

    return sum(acc), len(prediction), round(sum(acc) / len(sample) * 100, 2)


text = ''
while True:
    print('Print a random string containing 0 or 1:')
    user_str = input()
    text = update_text(text, user_str)
    if text_validation(text):
        break

print('Final data string:', text, '\n')

statistic = count_triplets(text)

test_str = ''
while len(test_str) < 4:
    print('Please enter a test string containing 0 or 1:')
    test_str = input()

prediction = make_prediction(test_str, statistic)
print('predictions:', prediction)

acc_score = accuracy(test_str, prediction)
print(f'Computer guessed {acc_score[0]} out of {acc_score[1]}'
      f' symbols right ({acc_score[2]} %)')
