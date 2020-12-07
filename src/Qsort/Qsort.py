import random
import neal

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
        self.__set_lam()

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

    def __set_lam(self):
        self.__lam = self.max_numbers/2

    def get_lam(self):
        return self.__lam

    def solutions2labels(self, solutions):
        self.results = []
        for sol in solutions:
            result = [0] * self.num_numbers
            if self.check_violation(sol):
                for ind_val, row in enumerate(self.__solution_matrix):
                    result[row.index(1)] = self.numbers[ind_val]
                self.results.append(result)
            else:
                continue
        return self.results

    def check_violation(self, solution):
        num_inc = self.num_numbers
        self.__solution_matrix = []
        num_violation = 0

        # solutionを行列に変形
        for num in range(self.num_numbers):
            self.__solution_matrix.append(solution[num*self.num_numbers:num_inc])
            num_inc += self.num_numbers

        # columnsに1が1個ずつかどうか
        for ind_col in range(self.num_numbers):
            tmp = 0
            for ind_row in range(self.num_numbers):
                tmp += self.__solution_matrix[ind_row][ind_col]
            if not tmp == 1:
                num_violation += 1

        # rowsに1が1個ずつかどうか
        for row in self.__solution_matrix:
            if not sum(row) == 1:
                num_violation += 1

        if not num_violation == 0:
            print(solution, "に制約違反が，", num_violation, "個見つかりました．")
            return False
        else:
            return True

    def get_solutions(self, response):
        self.response = response
        self.solutions = [
            state.tolist() 
            for i, state in enumerate(response.states) 
            if response.energies[i] == min(response.energies)
        ]
        return self.solutions

    def select_solutions(self):
        self.selected_sols = []
        for sol in self.solutions:
            if not sol in self.selected_sols:
                self.selected_sols.append(sol)
        return self.selected_sols

    def get_sorted_numbers(self):
        first_numbers = [num[0] for num in self.results]
        self.sorted_numbers = self.results[first_numbers.index(max(first_numbers))]
        return self.sorted_numbers

    def SAsolver(self, num_reads=100):
        sampler = neal.SASampler()
        self.response = sampler.sample_qubo(self.qubo, num_reads=num_reads)
        self.get_solutions(self.response)
        self.select_solutions()
        return self.get_sorted_numbers()