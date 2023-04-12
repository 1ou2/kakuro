import itertools
import collections
from functools import reduce
from typing import List

class KakuroData:
    def def __init__(self):
        self.factors = {}
        self.sum_by_len = {}
        self.len_by_sum = {}
        self.factors_by_sum = {}


    def find_combinations(self):
        # we get all the possible combinations that have 2 to 9 factors
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for length in range(2, 10):
            for combination in itertools.combinations(numbers, length):
                total_sum = sum(combination)
                factors_str = "".join(map(str, combination))
                self.len_by_sum[total_sum] = length
                self.factors_by_sum[total_sum] = factors_str

                

        
KakuroData.find_combinations()

