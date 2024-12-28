file_pwd = input()

with open(f'{file_pwd}') as f:
    content = f.readlines()

for i, row in enumerate(content):
    if len(row) > 79:
        print(f'Line {i + 1}: S001 Too long')
