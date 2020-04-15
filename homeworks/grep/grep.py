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
    elif params.line_number and not params.context:
        line_number(lines, params.pattern)
    elif params.context and not params.line_number:
        context_n(lines, params.pattern, params.context, area='every')
    elif params.before_context:
        context_n(lines, params.pattern, params.before_context, area='before')
    elif params.after_context:
        context_n(lines, params.pattern, params.after_context, area='after')
    elif params.line_number and params.context:
        context_n(lines, params.pattern, params.context, with_line_number=True)
    elif params.pattern:
        pattern_in_line(lines, params.pattern)


def pattern_in_line(lines: list, pattern: str):
    """Выводит строки, которые совпадают с шаблоном"""
    for line in lines:
        if pattern in line:
            output(line)


def invert(lines: list, pattern: str):
    """Выводит строки, которые НЕ совпадают с шаблоном"""
    for line in lines:
        if pattern not in line:
            output(line)


def ignore_case(lines: list, pattern: str):
    """При сравнении шаблона не учитывает регистр"""
    pattern = pattern.lower()
    lower_lines = [line.lower() for line in lines]
    for index in range(len(lower_lines)):
        if pattern in lower_lines[index]:
            output(lines[index])


def _count(lines: list, pattern: str):
    """Выводит только число строк удовлетворивших шаблону."""
    amount_lines = 0
    for line in lines:
        if pattern in line:
            amount_lines += 1
    output(f"{amount_lines}")


def line_number(lines: list, pattern: str):
    """Перед срокой выводит также и ее номер (строки нумеруются с единицы) в виде '5:строка'"""
    for number, line in enumerate(lines, 1):
        if pattern in line:
            output(f"{number}:{line}")


def context_n(lines: list, pattern: str, n: int, area: str = 'every', with_line_number: bool = False):
    """Помимо строки удовлетворяющей шаблону выводит также и N строк до и N строк после нее если столько есть.
    Если соседние блоки пересекаются то они объединяются. Если используется флаг line_number, то строки
    контекста нумеруются так "5-строка"
    """
    pattern_indexes = [index for index, line in enumerate(lines) if pattern in line]
    context_indexes = []

    for i in pattern_indexes:
        counter = n
        while counter > 0:
            if area == 'every' or area == 'before':
                before_index = i - counter
                if before_index not in pattern_indexes and before_index not in context_indexes and before_index >= 0:
                    context_indexes.append(before_index)
            if area == 'every' or area == 'after':
                after_index = i + counter
                if after_index not in pattern_indexes and after_index not in context_indexes and after_index <= len(lines):
                    context_indexes.append(after_index)
            counter -= 1

    if with_line_number:
        for index, line in enumerate(lines):
            if index in context_indexes:
                output(f"{index + 1}-{line}")
            elif index in pattern_indexes:
                output(f"{index + 1}:{line}")

    if not with_line_number:
        result_indexes = context_indexes + pattern_indexes
        result = [lines[index] for index in range(len(lines)) if index in result_indexes]
        for line in result:
            output(line)


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
        lines = ['vr', 'baab', 'abbb', 'fc', 'bbb', 'cc']
        grep(lines, params)


if __name__ == '__main__':
    main()
