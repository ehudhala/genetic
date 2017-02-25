import random

import itertools
import bisect
from typing import List, Tuple

from genetic.types import Chromosome, Fitness, Population


def proportionate_selection(population: Population, fitnesses: List[Fitness], rand: random.Random=None) -> Chromosome:
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


def select_chromosomes(population: Population, fitnesses: List[Fitness], amount: int) -> Tuple[Chromosome, ...]:
    """
    Gets a population, and selects from the population the amount of chromosomes wanted.
    The selection is a proportionate selection.
    Selection is done "with replacement" -
    meaning that the same chromosome can be selected more than once to become a parent.
    :param population: The population to select from.
    :param fitnesses: The fitness of each of the individuals in the population.
    :param amount: The amount of individuals to select.
    :return: The amount of requested chromosomes.
    """
    return tuple(proportionate_selection(population, fitnesses)
                 for _ in range(amount))

