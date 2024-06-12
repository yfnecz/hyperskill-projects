import csv
import time

class AlgorithmImdb:
    def __init__(self):
        self.filename = 'movies.csv'
        self.movies = []
        with open(self.filename, 'r') as cs_file:
            file_reader = csv.reader(cs_file, delimiter=",")
            for line in file_reader:
                self.movies.append([line[0], float(line[1])])
            cs_file.close()

    def bubble_sort(self):
        for _ in range(len(self.movies) - 1):
            for j in range(0, len(self.movies) - 1):
                if self.movies[j][1] > self.movies[j + 1][1]:
                    self.movies[j], self.movies[j + 1] = self.movies[j + 1], self.movies[j]

    def binary_search(self):
        left = 0
        right = len(self.movies) - 1
        while left <= right:
            middle = int((left + right) / 2)
            if self.movies[middle][1] == 6.0:
                return middle
            elif self.movies[middle][1] > 6.0:
                right = middle - 1
            else:
                left = middle + 1
        return -1
    
    def print_elems(self):
        left = self.binary_search()
        right = left
        while left > 0 and self.movies[left - 1][1] == 6.0:
            left -= 1
        while right < len(self.movies) - 1 and self.movies[right + 1][1] == 6.0:
            right += 1
        for i in range(left, right + 1):
            print(f'{self.movies[i][0]} - {self.movies[i][1]}')

    def merge(self, a, b):
        size_a = len(a)
        size_b = len(b)
        total = size_a + size_b
        ind_a, ind_b = 0, 0
        result = []
        for i in range(total):
            if ind_a < size_a and ind_b < size_b:
                if a[ind_a][1] < b[ind_b][1]:
                    result.append(a[ind_a])
                    ind_a += 1
                else:
                    result.append(b[ind_b])
                    ind_b += 1
            elif ind_a < size_a:
                result.append(a[ind_a])
                ind_a += 1
            else:
                result.append(b[ind_b])
                ind_b += 1
        return result

    def merge_sort(self, arr):
        size = len(arr)
        if size <= 1:
            return arr
        return self.merge(self.merge_sort(arr[size//2:]), self.merge_sort(arr[:size//2]))


if __name__ == '__main__':
    a = AlgorithmImdb()
    a.movies = a.merge_sort(a.movies)
    a.print_elems()
    
    
    