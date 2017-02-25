from typing import TypeVar, List

Locus = TypeVar('Locus', [int])
Chromosome = List[Locus]
Population = List[Chromosome]

Fitness = float
