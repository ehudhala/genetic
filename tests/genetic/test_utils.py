import random

import pytest
from genetic.utils import proportionate_selection


@pytest.fixture
def rand():
    return random.Random()


def test_proportion_select_doesnt_select_0_fitness(rand):
    """
    Tests that when the fitness of an individual is 0,
    it is not selected.
    """
    assert proportionate_selection('abcd', [1, 0, 0, 0]) == 'a'
    assert proportionate_selection('abcd', [0, 1, 0, 0]) == 'b'
    assert proportionate_selection('abcd', [0, 0, 1, 0]) == 'c'
    assert proportionate_selection('abcd', [0, 0, 0, 1]) == 'd'

@pytest.mark.parametrize(('random_choice', 'individual'), [
    (0.5, 'a'),
    (1.5, 'b'),
    (2.5, 'c'),
    (3.5, 'd')
])
def test_proportion_select_selects_where_random_falls(rand, random_choice, individual):
    """
    Tests that when the "random" falls in the slice of an individual,
    that individual is selected.
    """
    rand.uniform = lambda *a: random_choice
    assert proportionate_selection('abcd', [1] * 4, rand) == individual

def test_proportion_select_doesnt_fail_on_ends(rand):
    """
    Tests that even when the random falls on the ends (0 and the sum of the fitnesses)
    No exception is raised.
    """
    rand.uniform = lambda *a: 4
    assert proportionate_selection('abcd', [1] * 4, rand) == 'd'
    rand.uniform = lambda *a: 0
    assert proportionate_selection('abcd', [1] * 4, rand) == 'a'
