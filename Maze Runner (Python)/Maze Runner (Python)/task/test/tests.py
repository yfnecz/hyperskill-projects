from hstest import *
from enum import Enum
from typing import List


class Elem(Enum):
    WALL = '\u2588'
    EMPTY = ' '
    PATH = '/'
    DUMMY = ''

    @staticmethod
    def get(c):
        if c == '\u2588':
            return Elem.WALL
        if c == ' ':
            return Elem.EMPTY
        if c == '/':
            return Elem.PATH
        return


class MazeCheck:
    maze = []

    def __init__(self, lines: List[str]):
        if isinstance(lines, MazeCheck):
            self.maze = lines.maze.copy()
        else:
            line_count = 1
            for line in lines:
                if len(line) % 2 != 0:
                    raise WrongAnswer(
                        f'Line {line_count} of the maze contains odd number of characters. Should be always even.')
                for c in list(line):
                    if Elem.get(c) is None:
                        raise WrongAnswer(f'Found strange symbol in the {line_count} line of the maze: \\u{ord(c)}')
                line_width = int(len(line) / 2)
                for curr_width in range(0, line_width):
                    curr_index = curr_width * 2
                    next_index = curr_index + 1

                    curr_char = line[curr_index]
                    next_char = line[next_index]

                    if curr_char != next_char:
                        raise WrongAnswer(
                            f"There are symbols in this line that don't appear twice in a row (at indexes {curr_index} "
                            f"and {next_index}).\nLine: \"{line}\"")
                line_count += 1

            maze_width = int(len(lines[0]) / 2)
            maze_height = len(lines)

            line_count = 1
            for line in lines:
                if len(line) / 2 != maze_width:
                    raise WrongAnswer(
                        f"The first line of the maze contains {len(lines[0])} characters, but the line #{line_count} "
                        f"contains {len(line)} characters.")
                line_count += 1

            self.maze = [[Elem.DUMMY] * maze_width for i in range(0, maze_height)]

            for curr_height in range(0, maze_height):
                line = list(lines[curr_height])
                for curr_width in range(0, maze_width):
                    c = line[curr_width * 2]
                    self.maze[curr_height][curr_width] = Elem.get(c)

            if self.maze[0][0] != Elem.WALL or \
                    self.maze[0][maze_width - 1] != Elem.WALL or \
                    self.maze[maze_height - 1][0] != Elem.WALL or \
                    self.maze[maze_height - 1][maze_width - 1] != Elem.WALL:
                raise WrongAnswer(f"All four corners of the maze must be walls.")

            for h in range(0, maze_height - 2):
                for w in range(0, maze_width - 2):
                    if self.get_elem(h, w) == Elem.WALL and \
                            self.get_elem(h, w + 1) == Elem.WALL and \
                            self.get_elem(h, w + 2) == Elem.WALL and \
 \
                            self.get_elem(h + 1, w) == Elem.WALL and \
                            self.get_elem(h + 1, w + 1) == Elem.WALL and \
                            self.get_elem(h + 1, w + 2) == Elem.WALL and \
 \
                            self.get_elem(h + 2, w) == Elem.WALL and \
                            self.get_elem(h + 2, w + 1) == Elem.WALL and \
                            self.get_elem(h + 2, w + 2) == Elem.WALL:
                        raise WrongAnswer(
                            'There are 3x3 block in the maze consisting only of walls. Such blocks are not allowed.')

    def get_row(self, row_num):
        new_row = [Elem.DUMMY] * self.get_width()
        for i in range(0, self.get_width()):
            new_row[i] = self.maze[row_num][i]
        return new_row

    def get_col(self, col_num):
        new_col = [Elem.DUMMY] * self.get_height()
        for i in range(0, self.get_height()):
            new_col[i] = self.maze[i][col_num]
        return new_col

    def get_elem(self, height, width):
        return self.maze[height][width]

    def set_elem(self, height, width, elem):
        self.maze[height][width] = elem

    def get_width(self):
        return len(self.maze[0])

    def get_height(self):
        return len(self.maze)

    def copy(self):
        return MazeCheck(self)

    def count(self, to_count):
        sum_el = 0
        for row in self.maze:
            for e in row:
                if e == to_count:
                    sum_el += 1
        return sum_el

    def count_around(self, h, w, elem):
        sum_el = 0
        if h + 1 < self.get_height() and self.get_elem(h + 1, w) == elem:
            sum_el += 1
        if h - 1 >= 0 and self.get_elem(h - 1, w) == elem:
            sum_el += 1
        if w + 1 < self.get_width() and self.get_elem(h, w + 1) == elem:
            sum_el += 1
        if w - 1 >= 0 and self.get_elem(h, w - 1) == elem:
            sum_el += 1
        return sum_el

    def count_entrances(self):
        entrance_count = 0
        for line in [self.get_col(0),
                     self.get_col(self.get_width() - 1),
                     self.get_row(0),
                     self.get_row(self.get_height() - 1)]:
            for e in line:
                if e != Elem.WALL:
                    entrance_count += 1
        return entrance_count

    def propagate(self, fr, to):
        did_propagate = True
        while did_propagate:
            did_propagate = False
            for h in range(0, self.get_height()):
                for w in range(0, self.get_width()):
                    if self.get_elem(h, w) == fr:
                        if self.count_around(h, w, to) > 0:
                            did_propagate = True
                            self.set_elem(h, w, to)

    def check_accessibility(self):
        entrance_height = 0
        entrance_width = 0
        try:
            for curr_width in [0, self.get_width() - 1]:
                for curr_height in range(0, self.get_height()):
                    if self.get_elem(curr_height, curr_width) != Elem.WALL:
                        entrance_height = curr_height
                        entrance_width = curr_width
                        raise StopIteration
            for curr_height in [0, self.get_height() - 1]:
                for curr_width in range(0, self.get_width()):
                    if self.get_elem(curr_height, curr_width) != Elem.WALL:
                        entrance_height = curr_height
                        entrance_width = curr_width
                        raise StopIteration
        except StopIteration:
            pass
        copy = self.copy()
        copy.set_elem(entrance_height, entrance_width, Elem.PATH)
        copy.propagate(Elem.EMPTY, Elem.PATH)

        return copy.count(Elem.EMPTY)

    def check_path(self):
        entrance_height = 0
        entrance_width = 0

        for curr_width in [0, self.get_width() - 1]:
            for curr_height in range(0, self.get_height()):
                if self.get_elem(curr_height, curr_width) == Elem.EMPTY:
                    raise WrongAnswer('If the maze is solved all the entrances should be marked with \'//\' characters')
                if self.get_elem(curr_height, curr_width) == Elem.PATH:
                    entrance_height = curr_height
                    entrance_width = curr_width

        for curr_height in [0, self.get_height() - 1]:
            for curr_width in range(0, self.get_width()):
                if self.get_elem(curr_height, curr_width) == Elem.EMPTY:
                    raise WrongAnswer('If the maze is solved all the entrances should be marked with \'//\' characters')
                if self.get_elem(curr_height, curr_width) == Elem.PATH:
                    entrance_height = curr_height
                    entrance_width = curr_width

        for h in range(0, self.get_height()):
            for w in range(0, self.get_width()):
                if self.get_elem(h, w) == Elem.PATH:
                    if self.count_around(h, w, Elem.PATH) >= 3:
                        raise WrongAnswer("The escape path shouldn't branch off, it should go in one direction.")

        copy = self.copy()
        copy.set_elem(entrance_height, entrance_width, Elem.DUMMY)
        copy.propagate(Elem.PATH, Elem.DUMMY)

        return copy.count(Elem.PATH)

    def equals(self, other):
        if self.get_width() != other.get_width() or self.get_height() != other.get_height():
            return False
        for h in range(0, self.get_height()):
            for w in range(0, self.get_width()):
                if self.get_elem(h, w) == Elem.WALL and other.get_elem(h, w) != Elem.WALL or \
                        self.get_elem(h, w) != Elem.WALL and other.get_elem(h, w) == Elem.WALL:
                    return False
        return True

    @staticmethod
    def parse(text: str):
        mazes = []

        lines = text.splitlines()
        lines.append('')

        maze_lines = []

        is_started = False
        for line in lines:
            if '\u2588' in line:
                is_started = True
                maze_lines.append(line)
            else:
                if is_started:
                    is_started = False
                    maze = MazeCheck(maze_lines)
                    mazes.append(maze)
                    maze_lines.clear()
        return mazes


class Clue:
    def __init__(self, s: int, c: int, wp: bool):
        self.size = s
        self.count = c
        self.withPath = wp


class MazeRunnerTests(StageTest):
    test_data = [
        ["1 17 0", Clue(17, 1, False)],
        ["1 29 3 test_maze.txt 0", Clue(29, 1, False)],
        ["2 test_maze.txt 4 0", Clue(29, 1, False)],
        ["1 35 3 test_maze.txt 0", Clue(35, 1, False)],
        ["2 test_maze.txt 4 0", Clue(35, 1, False)],
        ["2 test_maze.txt 4 5 0", Clue(35, 2, True)]
    ]

    @dynamic_test(data=test_data)
    def test_exit(self, inp, clue):
        pr = TestedProgram()
        pr.start()

        output = ""

        for i in inp.split(' '):
            output += pr.execute(i)

        mazes = MazeCheck.parse(output)

        if len(mazes) == 0:
            return CheckResult.wrong(
                "No mazes found in the output. Check if you are using \\u2588 character to print the maze.")

        if len(mazes) != clue.count:
            if clue.count == 1:
                return CheckResult.wrong(f"Found {len(mazes)} mazes in the output. Should be only one maze.")
            else:
                return CheckResult.wrong(f"Found {len(mazes)} mazes in the output. Should be only two mazes.")

        fst = mazes[0]
        snd = mazes[1] if len(mazes) == 2 else None

        if not (snd is None) and not fst.equals(snd):
            return CheckResult.wrong("The two mazes shown should be equal, but they are different.")

        if fst.count(Elem.PATH) != 0:
            return CheckResult.wrong("The first maze should not contain '/' characters.")

        entrances = fst.count_entrances()
        if entrances != 2:
            return CheckResult.wrong(f"There are {entrances} entrances to the maze, should be only two.")

        empty_left = fst.check_accessibility()
        if empty_left > 0:
            return CheckResult.wrong(
                f"There are {empty_left} empty cells that are inaccessible from the entrance of the maze (or there is "
                f"no way from the entrance to the exit).")

        if fst.get_height() != clue.size:
            return CheckResult.wrong(
                f"Number of rows in the maze is incorrect. It's {fst.get_height()}, but should be {clue.size}")
        if fst.get_width() != clue.size:
            return CheckResult.wrong(
                f"Number of columns in the maze is incorrect. It's {fst.get_width()}, but should be {clue.size}")

        if not (snd is None) and clue.withPath:
            path_left = snd.check_path()
            if path_left > 0:
                return CheckResult.wrong(f"There are {path_left} escape path ('//') " +
                                         "cells that are separated from the escape path of the maze " +
                                         "(or there is a break somewhere in the escape path).")

        return CheckResult.correct()


if __name__ == '__main__':
    MazeRunnerTests().run_tests()
