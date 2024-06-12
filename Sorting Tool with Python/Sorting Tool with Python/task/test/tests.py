import re
from typing import List, Any

from hstest.testing.settings import Settings
from hstest import *


class SortingToolStage6Test(StageTest):

    def generate(self) -> List[TestCase]:
        Settings.allow_out_of_input = True
        return stage4_tests() + stage5_tests() + stage6_tests()

    def check(self, reply: str, clue: Any) -> CheckResult:
        filename_arg_idx = -1
        try:
            filename_arg_idx = clue.args.index('-outputFile')
        except ValueError:
            pass
        error_messages = reply
        if filename_arg_idx != -1:
            filename = clue.args[filename_arg_idx + 1]
            try:
                f = open(filename)
                reply = ''.join(f.readlines())
                f.close()
            except FileNotFoundError:
                return CheckResult.wrong(f'There is no output file {filename}')
        else:
            error_messages = ""
        if 'byCount' in clue.args:
            return self.by_count(reply, clue, error_messages)
        else:
            return self.natural(reply, clue, error_messages)

    def by_count(self, reply: str, clue: Any, error_messages: str):
        if 'long' in clue.args:
            return check_by_count(parse_long_tokens(clue.console_input), clue, reply, error_messages)
        elif 'word' in clue.args:
            return check_by_count(parse_word_tokens(clue.console_input), clue, reply, error_messages)
        elif 'line' in clue.args:
            return check_by_count(parse_line_tokens(clue.console_input), clue, reply, error_messages)
        else:
            return check_by_count([''], clue, reply, error_messages)

    def natural(self, reply: str, clue: Any, error_messages: str):
        if 'long' in clue.args:
            return check_natural(parse_long_tokens(clue.console_input), clue, reply, error_messages)
        elif 'word' in clue.args:
            return check_natural(parse_word_tokens(clue.console_input), clue, reply, error_messages)
        elif 'line' in clue.args:
            return check_natural(parse_line_tokens(clue.console_input), clue, reply, error_messages)
        else:
            return check_natural([''], clue, reply, error_messages)


class SortingToolClue:
    def __init__(self, console_input, reveal_test, args):
        self.console_input = console_input
        self.reveal_test = reveal_test
        self.args = args


def reveal_raw_test(clue, reply):
    return f"Args:\n{' '.join(clue.args)}\nInput:\n{clue.console_input}\nYour output:\n{reply}\n\n"


def create_test(console_input, reveal_test, args=None):
    if args is None:
        args = ['-dataType', 'long']
    if console_input == '':
        return TestCase(args=args, attach=SortingToolClue(console_input, reveal_test, args))
    return TestCase(args=args, stdin=console_input, attach=SortingToolClue(console_input, reveal_test, args))


def file_test_case(console_input, reveal_test, file, args=None):
    if args is None:
        args = ['-dataType', 'long']
    return TestCase(args=args, attach=SortingToolClue(console_input, reveal_test, args), files={
        file: console_input
    })



def stage4_tests() -> List[TestCase]:
    return [create_test('1 -2   333 4\n42\n1                 1'.strip(), True,
                        ['-dataType', 'long', '-sortingType', 'natural']),
            create_test('1 -2   333 4\n42\n1                 1'.strip(), True, ['-dataType', 'long']),
            create_test('1 -2   333 4\n42\n1                 1'.strip(), True,
                        ['-sortingType', 'byCount', '-dataType', 'long']),
            create_test('1 -2   333 4\n42\n1                 1'.strip(), True,
                        ['-sortingType', 'byCount', '-dataType', 'word']),
            create_test('1 -2   333 4\n42\n42\n1                 1'.strip(), True,
                        ['-sortingType', 'byCount', '-dataType', 'line']),
            create_test('1111 1111\n22222\n3\n44'.strip(), False, ['-sortingType', 'byCount', '-dataType', 'line']),
            create_test('1111 1111\n22222\n3\n44'.strip(), False, ['-sortingType', 'byCount', '-dataType', 'word']),
            create_test('1111 1111\n22222\n3\n44'.strip(), False, ['-sortingType', 'byCount', '-dataType', 'long'])]


def stage5_tests() -> List[TestCase]:
    return [create_test('', True, ['-sortingType']),
            create_test(''.strip(), True, ['-dataType']),
            create_test('1 -2   333 4\n42\n1                 1'.strip(), True,
                        ['-dataType', 'long', '-sortingType', 'byCount', '-abc']),
            create_test('1 -2   abc 4\nbcd\n1                 1'.strip(), True,
                        ['-dataType', 'long', '-sortingType', 'byCount']),
            create_test('1 -2   abc 4\nbcd\n1                 1'.strip(), True,
                        ['-dataType', 'line', '-sortingType', 'byCount']),
            create_test(''.strip(), False,
                        ['-sortingType', 'byCount', '-dataType']),
            create_test(''.strip(), False,
                        ['-dataType', 'line', '-sortingType']),
            create_test('1111 1111\n22222\n3\n44'.strip(), False,
                        ['-sortingType', 'byCount', '-dataType', 'line', '-bcd', '-cde']),
            create_test('1111 abc\nbcd\ncde\n44'.strip(), False,
                        ['-sortingType', 'byCount', '-dataType', 'long']),
            create_test('1111 abc\nbcd\ncde\n44'.strip(), False,
                        ['-sortingType', 'byCount', '-dataType', 'word']),
            ]


def stage6_tests() -> List[TestCase]:
    return [file_test_case('1 -2   333 4\n42\n1                 1'.strip(), True, 'input.txt',
                           ["-sortingType", "byCount", '-dataType', 'long', "-inputFile", "input.txt"]),
            file_test_case('1 -2   333 4\n42\n1                 1'.strip(), True, 'data.dat',
                           ["-sortingType", "byCount", '-dataType', 'long', "-inputFile", "data.dat", "-outputFile", "out.txt"]),
            file_test_case('1 -2   333 4\n42\n1                 1'.strip(), False, 'input.txt',
                           ["-sortingType", "natural", '-dataType', 'long', "-inputFile", "input.txt"]),
            file_test_case('1 -2   333 4\n42\n1                 1'.strip(), False, 'data.dat',
                           ["-sortingType", "natural", '-dataType', 'long', "-inputFile", "data.dat", "-outputFile", "out.txt"]),
            file_test_case('1 -2   333 4\n42\n1                 1'.strip(), False, 'data.dat',
                           ["-sortingType", '-dataType', 'long', "-inputFile", "data.dat", "-outputFile", "out.txt"]),
            file_test_case('1 -2   333 4\n42\n1                 1'.strip(), False, 'data.dat',
                           ["-sortingType", "natural", '-dataType', 'long', "-inputFile", "data.dat", "-outputFile", "out.txt", '-bcd', '-cde']),
            ]


def bad_args(args: List):
    if '-sortingType' in args and 'byCount' not in args and 'natural' not in args:
        return 'No sorting type defined!'
    if '-dataType' in args and 'long' not in args and 'word' not in args and 'line' not in args:
        return 'No data type defined!'
    ex = list(filter(lambda a: a not in ['-sortingType', 'byCount', 'natural', '-dataType', 'line', 'long', 'word',
                                         '-inputFile', '-outputFile', 'input.txt', 'out.txt', 'data.dat'],
                     args))
    if len(ex) != 0:
        return ' '.join(ex)
    return ''


def parse_long_tokens(inp):
    array = []
    for i in inp.split():
        try:
            array.append(int(i))
        except ValueError:
            array.append(i)
    return array


def parse_word_tokens(inp):
    return inp.split()


def parse_line_tokens(inp):
    return inp.splitlines()


def check_error_output(reason, reply):
    if reason == 'No sorting type defined!':
        if len(reply.splitlines()) == 1 and 'No sorting type defined!' in reply:
            raise TestPassed()
        else:
            raise WrongAnswer('If there is no sorting type defined in args, your program should output only one'
                              ' "No sorting type defined!" string and finish')

    if reason == 'No data type defined!':
        if len(reply.splitlines()) == 1 and 'No data type defined!' in reply:
            raise TestPassed()
        else:
            raise WrongAnswer('If there is no data type defined in args, your program should output only one'
                              ' "No data type defined!" string and finish')
    wrong_args = reason.split(' ')
    lines = reply.splitlines()
    if len(lines) < len(wrong_args):
        raise WrongAnswer('If there are wrong arguments provided, your program should output ""argument" is not'
                          ' a valid parameter. It will be skipped." string for each one')
    for i in range(0, len(wrong_args)):
        if wrong_args[i] not in lines[i]:
            raise WrongAnswer('If there are wrong arguments provided, your program should output ""argument" is not'
                              ' a valid parameter. It will be skipped." string for each one')
    return len(wrong_args)


def check_int(s):
    if s and s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def check_natural(actual_tokens, clue, reply, error_messages):
    output_file_errors_check = True
    if bad_args(clue.args) != '' and '-outputFile' in clue.args:
        if error_messages == "":
            return CheckResult.wrong(
                f"All of the error messages should be printed to the console")
        if "No sorting type defined!" in reply or "No data type defined!" in reply:
            return CheckResult.wrong(
                f"There should be no error messages printed in the output file")
        if ("No sorting type defined!" in error_messages or "No data type defined!" in error_messages) \
                and reply.strip() == "":
            return CheckResult.correct()
        wrong_args = bad_args(clue.args).split(' ')
        for i in range(0, len(wrong_args)):
            if wrong_args[i] in reply:
                return CheckResult.wrong(
                    f"There should be no error messages printed in the output file")
            if wrong_args[i] not in error_messages:
                return CheckResult.wrong(
                    f"All of the error messages should be printed to the console")
        output_file_errors_check = False

    amount_to_slice = 0
    if output_file_errors_check:
        if bad_args(clue.args) != '':
            amount_to_slice = check_error_output(bad_args(clue.args), reply)

        wrong_tokens = []
        if 'long' in clue.args:
            for i in actual_tokens:
                try:
                    int(i)
                except ValueError:
                    wrong_tokens.append(i)
            actual_tokens = list(filter(lambda a: isinstance(a, int), actual_tokens))
        reply = reply.strip()
        lines = reply.splitlines()

        if len(wrong_tokens) > len(lines):
            return CheckResult.wrong(
                'If there are wrong tokens provided, your program should output ""input_value" is not'
                ' a long. It will be skipped." string for each one')

        amount_to_slice += len(wrong_tokens)
        for i in range(0, len(wrong_tokens)):
            if wrong_tokens[i] not in lines[i]:
                return CheckResult.wrong(
                    'If there are wrong tokens provided, your program should output ""input_value" is not'
                    ' a long. It will be skipped." string for each one')

        lines = lines[amount_to_slice:]
    else:
        lines = reply.splitlines()

    if len(lines) != 2:
        if clue.reveal_test:
            return CheckResult.wrong(
                f"Can't parse your output for sorting naturally: expected 2 lines.\n"
                + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("Can't parse your output for sorting naturally: expected 2 lines.")

    total_match = re.search(r'(?P<total>\d+)', lines[0])
    if total_match is None:
        if clue.reveal_test:
            return CheckResult.wrong("The first line of your output after sorting naturally should contain a number\n"
                                     + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("The first line of your output after sorting naturally should contain a number")

    total = int(total_match.group('total'))
    actual_total = len(actual_tokens)

    if actual_total != total:
        if clue.reveal_test:
            return CheckResult.wrong(f"Total amount of tokens ({total}) is incorrect. Expected: {actual_total}.\n"
                                     + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong(
                "Printed total amount of tokens after sorting naturally is incorrect for some testcases")

    actual_tokens.sort()
    if ':' not in lines[1]:
        return CheckResult.wrong("Second line of your output for natural sort does not contain ':' character")
    sort_line = lines[1].split(':')[1].strip()

    for token in sort_line.split(' '):
        if not check_int(token):
            return CheckResult.wrong(
                "After ':' symbol there should be printed all the tokens, "
                "divided by space character for 'word' and 'long' data type.")
    sorted_tokens = parse_long_tokens(sort_line)

    if actual_total != len(sorted_tokens):
        if clue.reveal_test:
            return CheckResult.wrong(
                f"Total amount of sorted tokens ({len(sorted_tokens)}) is incorrect. Expected: {actual_total}.\n"
                + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("Total amount of sorted tokens is incorrect for some testcases.")
    if sorted_tokens != actual_tokens:
        if clue.reveal_test:
            return CheckResult.wrong(f"Some tokens were sorted incorrectly.\n"
                                     + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("Some tokens were sorted incorrectly.")

    return CheckResult.correct()


def check_by_count(actual_tokens, clue, reply, error_messages):
    output_file_errors_check = True
    if bad_args(clue.args) != '' and '-outputFile' in clue.args:
        if error_messages == "":
            return CheckResult.wrong(
                f"All of the error messages should be printed to the console")
        if "No sorting type defined!" in reply or "No data type defined!" in reply:
            return CheckResult.wrong(
                f"There should be no error messages printed in the output file")
        if ("No sorting type defined!" in error_messages or "No data type defined!" in error_messages) \
                and reply.strip() == "":
            return CheckResult.correct()
        wrong_args = bad_args(clue.args).split(' ')
        for i in range(0, len(wrong_args)):
            if wrong_args[i] in reply:
                return CheckResult.wrong(
                    f"There should be no error messages printed in the output file")
            if wrong_args[i] not in error_messages:
                return CheckResult.wrong(
                    f"All of the error messages should be printed to the console")
        output_file_errors_check = False

    amount_to_slice = 0
    if output_file_errors_check:
        if bad_args(clue.args) != '':
            amount_to_slice = check_error_output(bad_args(clue.args), reply)

        wrong_tokens = []
        if 'long' in clue.args:
            for i in actual_tokens:
                try:
                    int(i)
                except ValueError:
                    wrong_tokens.append(i)
            actual_tokens = list(filter(lambda a: isinstance(a, int), actual_tokens))
        reply = reply.strip()
        lines = reply.splitlines()

        if len(wrong_tokens) > len(lines):
            return CheckResult.wrong(
                'If there are wrong tokens provided, your program should output ""input_value" is not'
                ' a long. It will be skipped." string for each one')

        amount_to_slice += len(wrong_tokens)
        for i in range(0, len(wrong_tokens)):
            if wrong_tokens[i] not in lines[i]:
                return CheckResult.wrong(
                    'If there are wrong tokens provided, your program should output ""input_value" is not'
                    ' a long. It will be skipped." string for each one')

        lines = lines[amount_to_slice:]
    else:
        lines = reply.splitlines()

    if len(lines) == 0:
        if clue.reveal_test:
            return CheckResult.wrong("The first line of your output after sorting by count should contain a number\n"
                                     + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("The first line of your output after sorting by count should contain a number")

    total_match = re.search(r'(?P<total>\d+)', lines[0])
    if total_match is None:
        if clue.reveal_test:
            return CheckResult.wrong("The first line of your output after sorting by count should contain a number\n"
                                     + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("The first line of your output after sorting by count should contain a number")

    total = int(total_match.group('total'))
    actual_total = len(actual_tokens)

    if actual_total != total:
        if clue.reveal_test:
            return CheckResult.wrong(f"Total amount of tokens ({total}) is incorrect. Expected: {actual_total}.\n"
                                     + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong(
                "Printed total amount of tokens after sorting by count is incorrect for some testcases")

    sort = sorted(actual_tokens)
    sort = sorted(sort, key=lambda x: actual_tokens.count(x), reverse=False)
    token_to_count = dict.fromkeys(sort)
    for i in token_to_count.keys():
        token_to_count[i] = actual_tokens.count(i)

    actual_sorted_by_count = list(token_to_count)

    lines_with_tokens = lines[1:]

    if len(actual_sorted_by_count) != len(lines_with_tokens):
        if clue.reveal_test:
            return CheckResult.wrong(
                f"Amount of lines with tokens (after 'Total numbers:' line in byCount sort) ({len(lines_with_tokens)}) "
                f"is incorrect. Expected: {len(actual_sorted_by_count)}.\n"
                + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong(
                "Amount of lines with tokens (after 'Total numbers:' line in byCount sort) is incorrect")

    for i in range(0, len(lines_with_tokens)):
        if ':' not in lines_with_tokens[i]:
            return CheckResult.wrong("Each line with token in byCount sort should contain ':' character")
        token = lines_with_tokens[i].split(':')[0]
        info = lines_with_tokens[i].split(':')[1]

        info_match = re.search(r'(?P<count>\d+)\D+(?P<percentage>\d+)', info)
        count_actual_token = token_to_count[actual_sorted_by_count[i]]
        if info_match is None:
            if clue.reveal_test:
                return CheckResult.wrong(
                    f"Token ({lines_with_tokens[i]}) contains incorrect info. Expected: {actual_sorted_by_count[i]}: "
                    f"{count_actual_token} time(s), {int(count_actual_token / len(actual_tokens) * 100)}%.\n "
                    + reveal_raw_test(clue, reply))
            else:
                return CheckResult.wrong("Some of printed token lines in byCount sort contain incorrect info, or were "
                                         "not sorted correctly")
        token_count = info_match.group('count')
        token_percentage = info_match.group('percentage')

        if token != str(actual_sorted_by_count[i]) or token_count != str(count_actual_token) \
                or token_percentage != str(int(count_actual_token / len(actual_tokens) * 100)):
            if clue.reveal_test:
                return CheckResult.wrong(
                    f"Token ({lines_with_tokens[i]}) contains incorrect info. Expected: {actual_sorted_by_count[i]}: "
                    f"{count_actual_token} time(s), {int(count_actual_token / len(actual_tokens) * 100)}%.\n "
                    + reveal_raw_test(clue, reply))
            else:
                return CheckResult.wrong("Some of printed token lines in byCount sort contain incorrect info, or were "
                                         "not sorted correctly")

    return CheckResult.correct()


if __name__ == '__main__':
    SortingToolStage6Test().run_tests()
