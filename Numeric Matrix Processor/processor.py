n1, m1 = map(int, input().split())
matrix1 = [list(map(int, input().split())) for _ in range(n1)]
n2, m2 = map(int, input().split())
matrix2 = [list(map(int, input().split())) for _ in range(n2)]

# n1, m1 = 4, 5
# matrix1 = [[1, 2, 3, 4, 5],
#          [3, 2, 3, 2, 1],
#          [8, 0, 9, 9, 1],
#          [1, 3, 4, 5, 6]]
# n2, m2 = 4, 5
# matrix2 = [[1, 1, 4, 4, 5],
#          [4, 4, 5, 7, 8],
#          [1, 2, 3, 9, 8],
#          [1, 0, 0, 0, 1]]

if n1 == n2 and m1 == m2:
    matrix3 = [[matrix1[i][j] + matrix2[i][j] for j in range(m1)] for i in range(n1)]
    for row in matrix3:
        print(*row)
else:
    print("ERROR")
