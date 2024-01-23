"""simple arithmetic operations"""

text = input()
fn_text, operand, sn_text = text.split(' ')
first_number = int(fn_text)
second_number = int(sn_text)

if operand == '+':
    print(first_number + second_number)
elif operand == '-':
    print(first_number - second_number)
elif operand == '*':
    print(first_number * second_number)
