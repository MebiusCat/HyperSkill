import os
import re
import sys

error_key = {
    'S001': 'Too long',
    'S002': 'Indentation is not a multiple of four',
    'S003': 'Unnecessary semicolon',
    'S004': 'At least two spaces required before inline comments',
    'S005': 'TODO found (in comments only and case-insensitive)',
    'S006': 'More than two blank lines preceding a code line',
    'S007': 'Too many spaces after \'class\'',
    'S008': 'Class name should use CamelCase',
    'S009': 'Function name should use snake_case',
}

class ErrorChecker:
    def __init__(self, text, path=''):
        self.text = text
        self.result = {}
        self.path = path
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
        if self.rule_007(data):
            errors.append('S007')
        if self.rule_008(data):
            errors.append('S008')
        if self.rule_009(data):
            errors.append('S009')
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

    @staticmethod
    def rule_007(row):
        pattern = r'[class|def]\s{2,}\S'
        return bool(re.search(pattern, row))

    @staticmethod
    def rule_008(row):
        pattern = r'class [a-z]\w+:'
        return bool(re.search(pattern, row))

    @staticmethod
    def rule_009(row):
        pattern = r'def [A-Z]'
        return bool(re.search(pattern, row))


file_pwd = sys.argv[1]
if os.path.isdir(file_pwd):
    paths = []
    for root, dirs, files in os.walk(file_pwd, topdown=False):
        for name in files:
            if name[-3:] != '.py':
                continue
            paths.append(os.path.join(root, name))
else:
    paths = [file_pwd]

for path in sorted(paths):
    with open(f'{path}') as f:
        content = f.readlines()
    checker = ErrorChecker(content)
    for key, value in checker.result.items():
        if not value:
            continue
        for el in sorted(value):
            print(f'{f.name}: Line {key + 1}: {el} {error_key[el]}')
