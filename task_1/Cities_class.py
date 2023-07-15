import json
import random
from itertools import repeat, accumulate
from bisect import bisect

class Cities:
    def __init__(self, way: str) -> None:
        self.way = way


    def __get_data_list(self):
        with open(self.way, 'r',encoding='utf-8') as f:
            data = json.load(f)
        return data


    def __get_cities(self):
        cities = []
        for i in self.__get_data_list():
            cities.append(i['name'])
        return cities


    def __get_weights(self):
        weights = []
        for i in self.__get_data_list():
            weights.append(i['population'])
        return weights


    def choice_random_city(self):
        population = self.__get_cities()
        weights = self.__get_weights()
        n = len(population)
        hi = n - 1
        cum_weights = list(accumulate(weights))
        total = cum_weights[-1] + 0.0
        return [population[bisect(cum_weights, random.random() * total, 0, hi)]
             for i in repeat(None, 1)][0]

