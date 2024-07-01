'Compose a binary string'

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
    limit = 100
    count_symbols = len(_text)

    if count_symbols < limit:
        print(f'Current data length is {count_symbols}, {limit - count_symbols} symbols left')

    return len(_text) >= limit


text = ''
while True:
    print('Print a random string containing 0 or 1:')
    user_str = input()
    text = update_text(text, user_str)
    if text_validation(text):
        break

print('Final data string:', text)
