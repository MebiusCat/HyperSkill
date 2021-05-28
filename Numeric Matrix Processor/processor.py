class Matrix:
    def __init__(self):
        self.clear_data()

    def read_mtrx(self, test_n="", test_el=None):
        self.counter += 1
        adj = "first" if self.counter == 1 else "second"
        str_n = input(f"Enter size of {adj} matrix:") if test_n == "" else test_n
        n, m = map(int, str_n.split())

        if test_el is None:
            print(f"Enter {adj} matrix:")
            str_el = []
            for _ in range(n):
                str_el.append(input())
        else:
            str_el = test_el
        mtrx = [list(map(float, line.split())) for line in str_el]
        return mtrx, n, m

    def addition(self):
        if self.nA == self.nB and self.mA == self.mB:
            self.mtrx_R = [[self.mtrx_A[i][j] + self.mtrx_B[i][j] for j in range(self.mA)] for i in range(self.nA)]
            self.print_result()
        else:
            print("The operation cannot be performed.")

    def const_mult(self):
        mult_const = int(input('Enter constant: '))
        self.mtrx_R = [[self.mtrx_A[i][j] * mult_const for j in range(self.mA)] for i in range(self.nA)]
        self.print_result()

    def transpose(self, param):
        if param == '1':
            self.mtrx_R = [[self.mtrx_A[j][i] for j in range(self.mA)] for i in range(self.nA)]
        elif param == '2':
            self.mtrx_R = [[self.mtrx_A[j][i] for j in range(self.mA)][::-1] for i in range(self.nA)[::-1]]
        elif param == '3':
            self.mtrx_R = [self.mtrx_A[i][::-1] for i in range(self.nA)]
        elif param == '4':
            self.mtrx_R = [[self.mtrx_A[i][j] for j in range(self.mA)] for i in range(self.nA)[::-1]]
 
        self.print_result()

    def mult(self):
        if self.mA == self.nB:
            self.mtrx_R = [[sum([self.mtrx_A[i][k]*self.mtrx_B[k][j] for k in range(self.nB)]) for j in range(self.mB)] for i in range(self.nA)]
            self.print_result()
        else:
            print("ERROR")

    def print_result(self):
        print("The result is:")
        for row in self.mtrx_R:
            print(*row)

    def clear_data(self):
        self.mtrx_A, self.nA, self.mA = None, 0, 0
        self.mtrx_B, self.nB, self.mB = None, 0, 0
        self.mtrx_R, self.nR, self.mR = None, 0, 0
        self.counter = 0

    def main(self):
        while True:
            menu = ["1. Add matrices",
                    "2. Multiply matrix by a constant",
                    "3. Multiply matrices",
                    "4. Transpose matrix",
                    "0. Exit"]
            print(*menu, sep='\n')

            choice: str = input()
            print(f'Your choice: > {choice}')
            if choice == '1':
                self.mtrx_A, self.nA, self.mA = self.read_mtrx()
                self.mtrx_B, self.nB, self.mB = self.read_mtrx()
                self.addition()
            elif choice == '2':
                self.mtrx_A, self.nA, self.mA = self.read_mtrx()
                self.const_mult()
            elif choice == '3':
                self.mtrx_A, self.nA, self.mA = self.read_mtrx()
                self.mtrx_B, self.nB, self.mB = self.read_mtrx()
                self.mult()
            elif choice == '4':
                diag_menu = ["1. Main diagonal",
                             "2. Side diagonal",
                             "3. Vertical line",
                             "4. Horizontal line"]
                print(*diag_menu, sep='\n')
                diag_choice : str = input()
                self.mtrx_A, self.nA, self.mA = self.read_mtrx()
                self.transpose(diag_choice)
            elif choice == '0':
                print('Bye!')
                exit()
            else:
                print('Unknown option.')

#
# line_1 = '4 5'
# line_2 = ['1 2 3 4 5','3 2 3 2 1','8 0 9 9 1','1 3 4 5 6']
# line_3 = '4 5'
# line_4 = ['1 1 4 4 5','4 4 5 7 8','1 2 3 9 8','1 0 0 0 1']


line_1 = '3 3'
line_2 = ['1 7 7','6 6 4','4 2 1']
line_3 = '3 3'
line_4 = ['3 2 4','5 5 9','8 0 10']


# fabric = Matrix()
# fabric.mtrx_A, fabric.nA, fabric.mA = fabric.read_mtrx(line_1, line_2)
# # fabric.mtrx_B, fabric.nB, fabric.mB = fabric.read_mtrx(line_3, line_4)
# # fabric.mult()
# fabric.transpose('2')

fabric = Matrix()
fabric.main()
