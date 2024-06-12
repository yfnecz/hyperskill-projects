import numpy as np


class Tetris:
    def __init__(self, leng, wid):
        self.leng = leng
        self.wid = wid
        self.grid = np.empty((leng, wid), dtype=str)
        self.grid.fill('-')
        self.pieces = {'O': [[5, 6, 9, 10]],
                       'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
                       'S': [[6, 5, 9, 8], [5, 9, 10, 14]],
                       'Z': [[4, 5, 9, 10], [2, 5, 6, 9]],
                       'L': [[1, 5, 9, 10], [2, 4, 5, 6], [1, 2, 6, 10], [4, 5, 6, 8]],
                       'J': [[2, 6, 9, 10], [4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6]],
                       'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]}
        # O = [[4, 14, 15, 5]]
        # I = [[4, 14, 24, 34], [3, 4, 5, 6]]
        # S = [[5, 4, 14, 13], [4, 14, 15, 25]]
        # Z = [[4, 5, 15, 16], [5, 15, 14, 24]]
        # L = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
        # J = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
        # T = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]

    def print_grid(self, grid=None):
        print('')
        if grid is None:
            grid = self.grid
        for i in range(self.leng):
            print(' '.join(grid[i]))

    def print_piece(self, piece):
        if piece in self.pieces.keys():
            t.print_grid()
            places = self.pieces[piece]
            for j in range(5):
                grid = np.copy(self.grid)
                for i in places[j % len(places)]:
                    grid[i // 4][i % 4] = '0'
                self.print_grid(grid=grid)


if __name__ == '__main__':
    t = Tetris(4, 4)
    t.print_piece(input().strip())

