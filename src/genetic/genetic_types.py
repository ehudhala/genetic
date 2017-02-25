from typing import TypeVar, List, Callable, Tuple

Locus = TypeVar('Locus')
Chromosome = List[Locus]
Population = List[Chromosome]

Fitness = float
CrossoverFunction = Callable[[Chromosome, Chromosome], Tuple[Chromosome, Chromosome]]