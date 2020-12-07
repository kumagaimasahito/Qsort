import random

class Qsort:
    def __init__(self, numbers=None):
        if numbers != None:
            self.set_numbers(numbers)

    def set_random_numbers(self, num_numbers=4, min_rand=1, max_rand=100):
        self.numbers = [random.randint(min_rand, max_rand) for _ in range(num_numbers)]
        self.__set_parameters()

        print("index : numbers")
        for i, x in enumerate(self.numbers):
            print(i, "      : ", x)

    def set_numbers(self, numbers):
        self.numbers = numbers
        self.__set_parameters()

        print("index : numbers")
        for i, x in enumerate(self.numbers):
            print(i, "      : ", x)

    def __set_parameters(self):
        self.num_numbers = len(self.numbers)
        self.max_numbers = max(self.numbers)
        self.min_numbers = min(self.numbers)

    def set_qubo(self):
        self.__set_diffs()
        self.__set_neighbors()
        self.qubo = {
            ((v, i), (w, j)) : 
                self.__diffs[(v, w)] if (i, j) in self.__neighbors and (v, w) in self.__diffs.keys() else
                -2 * self.__lam if v == w and i == j else
                2 * self.__lam if v == w else
                2 * self.__lam if i == j else
                0
            for v in range(self.num_numbers)
            for w in range(v, self.num_numbers)
            for i in range(self.num_numbers)
            for j in range(self.num_numbers)
        }
        return self.qubo

    def __set_diffs(self):
        self.__diffs = {
            (v, w) : abs(self.numbers[w] - self.numbers[v]) 
            for v in range(self.num_numbers) 
            for w in range(v+1, self.num_numbers)
        }

    def get_diffs(self):
        print("pair         : difference")
        for pair, diff in self.__diffs.items():
            print(pair, "      : ", diff)
        return self.__diffs

    def __set_neighbors(self):
        self.__neighbors = [
            (i, j)
            for i in range(self.num_numbers) 
            for j in range(self.num_numbers)
            if abs(j-i) == 1
        ]

    def get_neighbors(self):
        print("neighbor")
        for pair in self.__neighbors:
            print(pair)
        return self.__neighbors

    def __sel_lam(self):
        self.__lam = self.max_numbers/2