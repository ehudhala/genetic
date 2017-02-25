import random

import itertools
import bisect
from typing import List, TypeVar

T = TypeVar('T')

def proportionate_selection(population: List[T], fitnesses: List[float], rand: random.Random=None) -> T:
    """
    In roulette wheel selection we receive a population of individuals,
    and select one of them (to be a parent) with proportion to their fitness.
    We conceptually slice a roulette wheel
    with each individual getting a slice as big as his fitness.
    :param population: The population to select from.
    :param fitnesses: The fitness of each of the individuals in the population.
    :return: A single individual of the population.
    """
    rand = rand or random

    accu_fitnesses = list(itertools.accumulate(fitnesses))
    chosen = rand.uniform(0, accu_fitnesses[-1])

    chosen_individual_index = min(bisect.bisect_right(accu_fitnesses, chosen), len(population) - 1)
    return population[chosen_individual_index]

