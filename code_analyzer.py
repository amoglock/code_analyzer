import re
import sys
import os

args = sys.argv
path = args[1]


class FileLine:
    blank_lines_counter = 0
    errors_list = list()

    def __init__(self, number, line, path_to_file):
        self.number = number
        self.line = line
        self.path_to_file = path_to_file

    def checking(self):
        long_line_check(self.line, self.number, self.path_to_file)
        bad_indentation_check(self.line, self.number, self.path_to_file)
        unnecessary_semicolon_check(self.line, self.number, self.path_to_file)
        comment_spaces_check(self.line, self.number, self.path_to_file)
        todo_comment_check(self.line, self.number, self.path_to_file)
        blank_lines_check(self.line, self.number, self.path_to_file)
        class_spase_check(self.line, self.number, self.path_to_file)
        class_name_check(self.line, self.number, self.path_to_file)
        func_name_check(self.line, self.number, self.path_to_file)


def scan_file(path_to_file):

    with open(path_to_file, 'r') as file:
        for number, line in enumerate(file):
            x = FileLine(number, line, path_to_file)
            x.checking()


def return_message(path_to_file, number, message):
    return f'{path_to_file}: Line {number + 1}: {message}'


def long_line_check(line, number, path_to_file):
    try:
        assert len(line.rstrip()) < 80, return_message(path_to_file, number, 'S001 Too Long')
    except AssertionError as err:
        FileLine.errors_list.append(err)


def bad_indentation_check(line, number, path_to_file):
    indentation_number = (len(line.rstrip()) - len(line.strip()))
    try:
        assert indentation_number % 4 == 0, return_message(path_to_file, number, 'S002 Indentation is bad')
    except AssertionError as err:
        FileLine.errors_list.append(err)


def unnecessary_semicolon_check(line, number, path_to_file):
    line = line.split('#')[0].rstrip()
    try:
        assert not line.endswith(';'), return_message(path_to_file, number, 'S003 Unnecessary semicolon')
    except AssertionError as err:
        FileLine.errors_list.append(err)


def comment_spaces_check(line, number, path_to_file):
    line = line.split('#', maxsplit=1)
    message = 'S004 At least two spaces required before inline comments'
    try:
        if line[1] and len(line[0]) > 0:
            assert line[0][-2:] == '  ', return_message(path_to_file, number, message)
    except AssertionError as err:
        FileLine.errors_list.append(err)
    except IndexError:
        pass


def todo_comment_check(line, number, path_to_file):
    try:
        comment = line.split('#', maxsplit=1)[1].rstrip()
        assert 'todo' not in comment.lower(), return_message(path_to_file, number, 'S005 TODO found')
    except AssertionError as err:
        FileLine.errors_list.append(err)
    except IndexError:
        pass


def blank_lines_check(line, number, path_to_file):
    message = 'S006 More than two blank lines used before this line'
    if len(line.strip()) == 0:
        FileLine.blank_lines_counter += 1
    else:
        FileLine.blank_lines_counter = 0
    try:
        assert FileLine.blank_lines_counter != 3, return_message(path_to_file, number + 1, message)
    except AssertionError as err:
        FileLine.errors_list.append(err)


def class_spase_check(line, number, path_to_file):
    template = r'(class)\s\s+|(def)\s\s+'
    result = re.match(template, line.strip())
    if result:
        name = result.group().strip()
        print(f'{path_to_file}: Line {number + 1}: S007 Too many spaces after \'{name}\'')


def class_name_check(line, number, path_to_file):
    template = r'class\s([a-z]\w*)'
    result = re.match(template, line.strip())
    if result:
        class_name = result.group(1)
        print(f'{path_to_file}: Line {number + 1}: S008 Class name \'{class_name}\' should use CamelCase')


def func_name_check(line, number, path_to_file):
    template = r'def\s([A-Z]\w*)'
    result = re.match(template, line.strip())
    if result:
        def_name = result.group(1)
        print(f'{path_to_file}: Line {number + 1}: S009 Function name \'{def_name}\' should use should use snake_case')


def main():
    if os.path.isdir(path):
        for name in os.listdir(path):
            scan_file(os.path.join(path, name))
    if os.path.isfile(path):
        scan_file(path)


if __name__ == '__main__':
    main()


for error_line in FileLine.errors_list:
    print(error_line)
