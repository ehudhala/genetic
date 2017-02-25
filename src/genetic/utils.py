import bisect
import itertools
import random
from typing import List, Tuple, Callable

from genetic.types import Chromosome, Fitness, Population, CrossoverFunction


# Selection

def proportionate_selection(population: Population, fitnesses: List[Fitness],
                            rand=None) -> Chromosome:
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

    chosen_individual_index = bisect.bisect_right(accu_fitnesses, chosen)
    chosen_individual_index = min(chosen_individual_index, len(population) - 1)
    return population[chosen_individual_index]


def select_chromosomes(population: Population, fitnesses: List[Fitness],
                       amount: int) -> Tuple[Chromosome, ...]:
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


# Crossover

def crossover(chrom_a: Chromosome, chrom_b: Chromosome, actual_crossover: CrossoverFunction,
              crossover_rate: float, rand: random.Random=None) -> Tuple[Chromosome, Chromosome]:
    """
    Gets two chromosomes, and crosses them over.
    There is a (high) chance that they will "mate" and create two offspring,
    and a chance that they will survive and continue to the next generation.
    :param chrom_a: The first chromosome.
    :param chrom_b: The second chromosome.
    :param actual_crossover: The crossover function that will happen if they "mate".
    :return: Two offspring chromosomes.
    :param crossover_rate: The rate at which chromosomes actually cross over.
    """
    rand = rand or random

    if rand.random() < crossover_rate:
        return actual_crossover(chrom_a, chrom_b)
    else:
        return chrom_a, chrom_b


def generation(population: Population, fitness: Callable[[Chromosome], Fitness],
               actual_crossover: CrossoverFunction, crossover_rate: float,
               mutator: Callable[[Chromosome], Chromosome]) -> Population:
    """
    Performs a single generation of the algorithm.
    In a generation we create a new population with the same size.
    We proportionately select (with replacement) two chromosomes,
    cross them over and mutate the offspring until our population is big enough.
    The reason this function has so many parameters is because this is the function
    to run on any genetic algorithm.
    :param population: The population to pass through one generation.
    :param fitness: The fitness function to get the fitness of a chromosome.
    :param actual_crossover: The function that gets two chromosomes, and actually crosses them over.
    :param crossover_rate: The rate at which Crossover will happen.
    :param mutator: The function that receives a chromosomes and mutates it (randomly)
    :return: The population after one generation.
    """
    fitnesses = list(map(fitness, population))

    new_population = []
    while len(new_population) < len(population):
        chrom_a, chrom_b = select_chromosomes(population, fitnesses, 2)

        offspring = crossover(chrom_a, chrom_b, actual_crossover, crossover_rate)

        new_population.extend(map(mutator, offspring))

    return new_population

