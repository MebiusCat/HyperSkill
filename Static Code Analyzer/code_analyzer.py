error_key = {
    'S001': 'Too long',
    'S002': 'Indentation is not a multiple of four',
    'S003': 'Unnecessary semicolon',
    'S004': 'At least two spaces required before inline comments',
    'S005': 'TODO found (in comments only and case-insensitive)',
    'S006': 'More than two blank lines preceding a code line',
}

class ErrorChecker:
    def __init__(self, text):
        self.text = text
        self.result = {}

        self.check_data()

    def check_data(self):
        for i, line in enumerate(self.text):
            self.result.setdefault(i, [])
            if line:
                checking = self.check_row(line)
                if checking:
                    self.result[i].extend(checking)
        err_006 = self.rule_006()
        for elem in err_006:
            self.result[elem].extend(
                ['S006'])


    def check_row(self, data):
        errors = []
        if self.rule_001(data):
            errors.append('S001')
        if self.rule_002(data):
            errors.append('S002')
        if self.rule_003(data):
            errors.append('S003')
        if self.rule_004(data):
            errors.append('S004')
        if self.rule_005(data):
            errors.append('S005')
        return errors

    @staticmethod
    def rule_001(row):
        return len(row) > 79

    @staticmethod
    def rule_002(row):
        return row.strip() and (len(row) - len(row.lstrip())) % 4 != 0

    @staticmethod
    def rule_003(row):
        if not row.strip() or row.strip().startswith("#"):
            return False

        before_comment = row.strip().split("#", 1)[0].strip()

        if before_comment.endswith(";") and not before_comment.endswith("\\;"):
            return True

        return False

    @staticmethod
    def rule_004(row):
        if "#" not in row:
            return False
        idx = row.index("#")
        if idx and row[idx-2: idx] != '  ':
            return True
        return False

    @staticmethod
    def rule_005(row):
        if "#" in row:
            comment = row.split("#", 1)[1].strip()
            if "TODO" in comment.upper():
                return True
        return False

    def rule_006(self):
        errors = []
        blank_line_count = 0

        for i, line in enumerate(self.text):
            row = line.strip()

            if not row:
                blank_line_count += 1
            else:
                if blank_line_count > 2:
                    errors.append(i)
                blank_line_count = 0
        return errors

file_pwd = input()
# file_pwd = '../data/file.txt'
with open(f'{file_pwd}') as f:
    content = f.readlines()

checker = ErrorChecker(content)
for key, value in checker.result.items():
    if value:
        for el in value:
            print(f'Line {key + 1}: {el} {error_key[el]}')
