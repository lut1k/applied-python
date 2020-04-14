import argparse
import sys

COMBAT_MODE = False


def output(line):
    print(line)


def grep(lines, params):
    """Функция фильтрует строки, поступающие на стандартный вход и фильтрует их, согласно параметрам."""
    if COMBAT_MODE:
        lines = [line.strip() for line in lines]
    if params.invert:
        invert(lines, params.pattern)
    elif params.ignore_case:
        ignore_case(lines, params.pattern)
    elif params.count:
        _count(lines, params.pattern)
    elif params.pattern:
        pattern_in_line(lines, params.pattern)


def pattern_in_line(lines, pattern):
    """Выводит строки, которые совпадают с шаблоном"""
    for line in lines:
        if pattern in line:
            output(line)


def invert(lines, pattern):
    """Выводит строки, которые НЕ совпадают с шаблоном"""
    for line in lines:
        if pattern not in line:
            output(line)


def ignore_case(lines, pattern):
    """При сравнении шаблона не учитывает регистр"""
    pattern = pattern.lower()
    lower_lines = [line.lower() for line in lines]
    for index in range(len(lower_lines)):
        if pattern in lower_lines[index]:
            output(lines[index])


def _count(lines, pattern):
    """Выводит только число строк удовлетворивших шаблону."""
    amount_lines = 0
    for line in lines:
        if pattern in line:
            amount_lines += 1
    output(f"{amount_lines}")


def line_number(lines, pattern):
    """Перед срокой выводит также и ее номер (строки нумеруются с единицы) в виде '5:строка'"""
    pass


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v',
        action="store_true",
        dest="invert",
        default=False,
        help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i',
        action="store_true",
        dest="ignore_case",
        default=False,
        help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    if COMBAT_MODE:
        grep(sys.stdin.readlines(), params)
    else:
        grep(['baab', 'bbb', 'ccc', 'A'], params)


if __name__ == '__main__':
    main()
