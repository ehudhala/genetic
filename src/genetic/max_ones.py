import random
from typing import Tuple, Callable

from genetic.genetic_types import Locus, Chromosome, Population, Fitness
from genetic.utils import generation

RUNS = 20
GENERATIONS = 50
POPULATION_SIZE = 100
CHROMOSOME_LENGTH = 20

CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001


# Population

def create_random_chromosome(length: int=CHROMOSOME_LENGTH, rand=None) -> Chromosome:
    """
    Creates a random chromosome for our population.
    A chromosome is a list of either 0s or 1s.
    :param length: The length of the chromosome to create.
    :param rand: A random instance used for the randomness.
    :return: A chromosome
    """
    rand = rand or random
    return [round(rand.random()) for _ in range(length)]


def create_population(population_size: int=POPULATION_SIZE) -> Population:
    """
    Creates a random population of chromosome to begin with.
    :param population_size: The size of the population.
    """
    return [create_random_chromosome() for _ in range(population_size)]


# Crossover

def crossover_chromosomes(chrom_a: Chromosome, chrom_b: Chromosome,
                          rand=None) -> Tuple[Chromosome, Chromosome]:
    """
    Gets two chromosomes, and actually crosses them over, creating two offsprings.
    :param chrom_a: The first chromosome.
    :param chrom_b: The second chromosome.
    :return: Two offspring chromosomes.
    """
    rand = rand or random

    crossover_point = rand.randint(0, len(chrom_a))

    offspring_a = chrom_a[:crossover_point] + chrom_b[crossover_point:]
    offspring_b = chrom_b[:crossover_point] + chrom_a[crossover_point:]
    return offspring_a, offspring_b


# Mutation

def mutate_locus(locus: Locus, mutation_rate: float=MUTATION_RATE, rand=None) -> Locus:
    """
    Gets a locus, currently either 0 or 1, and mutates it.
    The mutation happens at a low rate, and if it does it flips the bit.
    :param locus: The locus to mutate.
    :param mutation_rate: The rate at which to mutate.
    :return: The new locus.
    """
    rand = rand or random

    return 1 ^ locus if rand.random() < mutation_rate else locus


def mutate(chromosome: Chromosome, locus_mutator: Callable[[Locus], Locus]=mutate_locus) -> Chromosome:
    """
    Gets a chromosome, and mutates it.
    The mutation happens at random to some of the locuses of the given chromosome.
    :param chromosome: The chromosome to mutate.
    :param locus_mutator: The mutate function, will run on all
    :return:
    """
    return list(map(locus_mutator, chromosome))


# Fitness

def count_ones(chromosome: Chromosome) -> Fitness:
    """
    This is our fitness function.
    A chromosome is more fit the more ones it has.
    :param chromosome: The chromosome to check the fitness of.
    :return: The fitness of the chromosome (the amount of ones)
    """
    return sum(chromosome)


# Genetic algorithm run

def max_ones_run(population: Population, generations: int=GENERATIONS):
    """
    Performs a run of a genetic algorithm to maximize ones on the given population.
    Should return chromosomes with mostly ones.
    :param generations: The amount of generations to run.
    :param population: The beginning population.
    :return: The population after the algorithm was run.
    """
    for i in range(generations):
        population = generation(population, count_ones, crossover_chromosomes, CROSSOVER_RATE, mutate)

    return population


if __name__ == '__main__':
    population = create_population()
    population = max_ones_run(population)
    print(population)

