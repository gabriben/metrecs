from typing import Any
import numpy as np


def retrieval_diversity(items: np.ndarray, distance_function: Any) -> float:
    """Smyth and McClave [2001]
    * Source: https://link.springer.com/chapter/10.1007/3-540-44593-5_25
    * Measure the intra-list diversity of a recommendation list R(|R|>1) as the average pairwise distance between items:
        Diversity(R) = ( sum_{i∈R} sum_{j∈R\{i}} dist(i, j) )  / ( |R|(|R|-1) )

    Args:
        items (np.ndarray): {array-like, sparse matrix} of shape (n_samples_X, n_features)
        distance_function(X): function to compute the pairwise distances of items vector representations

    Returns:
        float: retrieval_diversity score
    """
    R = items.shape[0]
    # Less than or equal to 1 items in recommendation list
    if R <= 1 or len(items.shape) == 1:
        diversity = np.nan
    else:
        pairwise_distances = distance_function(items)
        diversity = np.sum(pairwise_distances) / (R * (R - 1))
    return diversity
