import argparse


class SortingTool:
    def __init__(self):
        self.data = []
        self.i_file_name = None
        self.o_file_name = None
        parser = argparse.ArgumentParser()
        parser.add_argument('-dataType', nargs="?", choices=['long', 'word', 'line'], default='word')
        parser.add_argument('-sortingType', nargs="?", choices=['natural', 'byCount'], default='natural')
        parser.add_argument('-inputFile')
        parser.add_argument('-outputFile')
        args, unknown = parser.parse_known_args()
        for i in unknown:
            print(f'"-{i}" is not a valid parameter. It will be skipped.')
        args = vars(args)
        if not args['dataType']:
            raise ValueError("No data type defined!")
        if not args['sortingType']:
            raise ValueError("No sorting type defined!")
        if args['inputFile']:
            self.i_file_name = args['inputFile']
            self.i_file = open(self.i_file_name, 'r')
        if args['outputFile']:
            self.o_file_name = args['outputFile']
        self.type = args['dataType']
        self.sort_type = args['sortingType']

    def read_line(self):
        if self.i_file_name:
            line = self.i_file.readline()
            if line:
                return line
            raise EOFError
        else:
            return input()

    def write_line(self, line):
        if self.o_file_name:
            self.o_file.write(line + '\n')
        else:
            print(line)

    def read_input(self):
        while True:
            try:
                if self.type == 'word':
                    self.data.extend([x for x in self.read_line().split()])
                elif self.type == 'long':
                    my_list = [x for x in self.read_line().split()]
                    for x in my_list:
                        try:
                            self.data.extend([int(x)])
                        except ValueError:
                            print(f'"{x}" is not a long. It will be skipped.')
                else:
                    self.data.append(self.read_line())
            except EOFError:
                break

    def print_results(self):
        if self.o_file_name:
            self.o_file = open(self.o_file_name, 'w')
        dot_line = '.'
        if self.type == 'long':
            elem = 'numbers'
        else:
            elem = self.type + 's'
        if self.type == 'line':
            dot_line = ''
        self.write_line(f'Total {elem}: {len(self.data)}{dot_line}')
        if self.sort_type == 'natural':
            if self.type == 'line':
                self.write_line("Sorted data:")
                self.write_line('\n'.join(sorted(self.data)))
            else:
                self.write_line(f"Sorted data: {' '.join(str(x) for x in sorted(self.data))}")
        else:
            my_set = set(self.data)
            my_dict = {x: self.data.count(x) for x in my_set}
            for key, value in sorted(sorted(my_dict.items()), key=lambda v:v[1]):
                percent = int(value / len(self.data) * 100)
                self.write_line(f'{key}: {value} time(s), {percent}%')
        if self.i_file_name:
            self.i_file.close()
        if self.o_file_name:
            self.o_file.close()



if __name__ == '__main__':
    try:
        s = SortingTool()
        s.read_input()
        s.print_results()
    except ValueError as err:
        print(err)

