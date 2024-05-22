"""Let's draw some tree"""


def draw_a_tree(mtrx, y, span, pos_x, pos_y):
    mtrx[pos_x][pos_y + y - 1: pos_y + y] = 'X'
    mtrx[pos_x + 1][pos_y + y - 1: pos_y + y] = '^'

    idx = 0
    for i in range(1, y):
        mid = ''
        for j in range(2 * i - 1):
            mid += 'O' if j % 2 and not idx % span else '*'
            idx += 1 if j % 2 else 0

        mtrx[pos_x + i + 1][pos_y + y - i - 1: pos_y + y + i] = '/' + mid + '\\'
    mtrx[pos_x + y + 1][pos_y + y - 2:pos_y + y + 1] = '| |'


my_input = list(map(int, input().split()))
wth, hgt = 50, 30


if len(my_input) < 4:
    height, span = my_input
    mtrx = [[' ' for j in range(height)] for i in range(height + 2)]
    draw_a_tree(mtrx, height, span, 0, 0)

else:
    mtrx = [["|" if j in (0, wth - 1) else ' ' for j in range(wth)] for i in range(hgt)]
    mtrx[0] = ['-'] * wth
    mtrx[-1] = ['-'] * wth
    mtrx[27][20:30] = 'Merry Xmas'

    for k in range(len(my_input) // 4):
        height, span, pos_x, pos_y = my_input[4 * k: 4 * k + 4]
        pos_y -= height - 1
        draw_a_tree(mtrx, height, span, pos_x, pos_y)
print(*[''.join(r) for r in mtrx], sep='\n')
