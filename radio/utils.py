import math
import pandas as pd
import numpy as np
from numpy.typing import ArrayLike
from typing import Dict


def harmonic_number(n):
    """Returns an approximate value of n-th harmonic number.
    http://en.wikipedia.org/wiki/Harmonic_number
    """
    # Euler-Mascheroni constant
    gamma = 0.57721566490153286060651209008240243104215933593992
    return gamma + math.log(n) + 0.5 / n - 1.0 / (12 * n**2) + 1.0 / (120 * n**4)


# =====


def compute_distr(items, adjusted=False):
    """
    Calibration

    Compute the genre distribution for a given list of Items.
    """
    n = len(items)
    sum_one_over_ranks = harmonic_number(n)
    count = 0
    distr = {}
    for _, item in items.iterrows():
        count += 1
        topic_freq = distr.get(item.category, 0.0)
        distr[item.category] = (
            topic_freq + 1 * 1 / count / sum_one_over_ranks
            if adjusted
            else topic_freq + 1 * 1 / n
        )
    return distr


def compute_distr(items, adjusted=False):
    """
    FRAGMENTATION

    Compute the genre distribution for a given list of Items.
    """
    n = len(items)
    sum_one_over_ranks = harmonic_number(n)
    count = 0
    distr = {}
    for indx, item in enumerate(items):
        rank = indx + 1
        story_freq = distr.get(item, 0.0)
        distr[item] = (
            story_freq + 1 * 1 / rank / sum_one_over_ranks
            if adjusted
            else story_freq + 1 * 1 / n
        )
        count += 1

    return distr


def compute_distribution(
    a: np.ndarray[str],
    weights: np.ndarray[float] = [],
    distribution: Dict[str, float] = {},
) -> Dict:
    """_summary_
    Args:
        a (np.ndarray[str]): _description_
        weights (np.ndarray[float], optional): _description_. Defaults to [].
        distribution (Dict[str, float], optional): _description_. Defaults to {}.
    Returns:
        Dict: _description_
    >>> a = np.array(["a", "b", "c", "c"])
    >>> w1 = np.array([1 / harmonic_number(val) for i, val in enumerate(range(1, len(a) + 1))])
    >>> w2 = np.array([1 / rank / harmonic_number(len(a)) for rank in range(1, len(a) + 1)])
    >>> compute_distribution(a, weights=weights_jk)
        {'a': 0.997789233416392, 'b': 0.6666442916569965, 'c': 1.0254528751419092}
    >>> compute_distribution(a, weights=weights_radio)
        {'a': 0.4799997900047559, 'b': 0.23999989500237795, 'c': 0.2799998775027743}
    >>> compute_distr(a, False)
        {'a': 0.25, 'b': 0.25, 'c': 0.5}
    """
    distr = {} if not distribution else distribution
    weights = weights if np.any(weights) else np.ones(len(a)) / len(a)
    for item, weight in zip(a, weights):
        distr[item] = weight + distr.get(item, 0.0)
    return distr


a = np.array(["a", "b", "c", "c"])
weights_jk = np.array(
    [1 / harmonic_number(val) for i, val in enumerate(range(1, len(a) + 1))]
)
weights_radio = np.array(
    [1 / rank / harmonic_number(len(a)) for rank in range(1, len(a) + 1)]
)

compute_distribution(a, weights=weights_jk)
compute_distribution(a, weights=weights_radio)
compute_distr(a, True)

compute_distribution(a, distribution={})
compute_distr(a, False)
