"""
Algorithm Registry - Central registry for all algorithms
"""
from algorithms.sorting.bubble_sort import bubble_sort, get_algorithm_info as bubble_info
from algorithms.sorting.selection_sort import selection_sort, get_algorithm_info as selection_info
from algorithms.sorting.insertion_sort import insertion_sort, get_algorithm_info as insertion_info
from algorithms.sorting.merge_sort import merge_sort, get_algorithm_info as merge_info
from algorithms.sorting.quick_sort import quick_sort, get_algorithm_info as quick_info
from algorithms.sorting.heap_sort import heap_sort, get_algorithm_info as heap_info
from algorithms.searching.linear_search import linear_search, get_algorithm_info as linear_info
from algorithms.searching.binary_search import binary_search, get_algorithm_info as binary_info
from algorithms.searching.dfs import dfs, get_algorithm_info as dfs_info
from algorithms.searching.bfs import bfs, get_algorithm_info as bfs_info
from algorithms.dp.fibonacci import fibonacci, get_algorithm_info as fib_info
from algorithms.dp.knapsack import knapsack, get_algorithm_info as knapsack_info
from algorithms.dp.lcs import lcs, get_algorithm_info as lcs_info
from algorithms.dp.coin_change import coin_change, get_algorithm_info as coin_info
from algorithms.graph.graph_dfs import graph_dfs, get_algorithm_info as graph_dfs_info
from algorithms.graph.graph_bfs import graph_bfs, get_algorithm_info as graph_bfs_info
from algorithms.graph.dijkstra import dijkstra, get_algorithm_info as dijkstra_info
from algorithms.graph.prim import prim, get_algorithm_info as prim_info
from algorithms.graph.kruskal import kruskal, get_algorithm_info as kruskal_info


# Registry of all available algorithms
ALGORITHMS = {
    'Sorting Algorithms': {
        'Bubble Sort': {
            'function': bubble_sort,
            'info': bubble_info()
        },
        'Selection Sort': {
            'function': selection_sort,
            'info': selection_info()
        },
        'Insertion Sort': {
            'function': insertion_sort,
            'info': insertion_info()
        },
        'Merge Sort': {
            'function': merge_sort,
            'info': merge_info()
        },
        'Quick Sort': {
            'function': quick_sort,
            'info': quick_info()
        },
        'Heap Sort': {
            'function': heap_sort,
            'info': heap_info()
        },
    },
    'Searching Algorithms': {
        'Linear Search': {
            'function': linear_search,
            'info': linear_info()
        },
        'Binary Search': {
            'function': binary_search,
            'info': binary_info()
        },
        'DFS': {
            'function': dfs,
            'info': dfs_info()
        },
        'BFS': {
            'function': bfs,
            'info': bfs_info()
        },
    },
    'Dynamic Programming': {
        'Fibonacci': {
            'function': fibonacci,
            'info': fib_info()
        },
        'Knapsack Problem': {
            'function': knapsack,
            'info': knapsack_info()
        },
        'Longest Common Subsequence': {
            'function': lcs,
            'info': lcs_info()
        },
        'Coin Change': {
            'function': coin_change,
            'info': coin_info()
        },
    },
    'Graph Algorithms': {
        'Graph DFS': {
            'function': graph_dfs,
            'info': graph_dfs_info()
        },
        'Graph BFS': {
            'function': graph_bfs,
            'info': graph_bfs_info()
        },
        "Dijkstra's Algorithm": {
            'function': dijkstra,
            'info': dijkstra_info()
        },
        "Prim's Algorithm": {
            'function': prim,
            'info': prim_info()
        },
        "Kruskal's Algorithm": {
            'function': kruskal,
            'info': kruskal_info()
        },
    }
}


def get_algorithm(category, name):
    """
    Get algorithm function and info by category and name

    Args:
        category: Algorithm category
        name: Algorithm name

    Returns:
        Tuple of (algorithm_function, algorithm_info) or (None, None)
    """
    if category in ALGORITHMS and name in ALGORITHMS[category]:
        algo = ALGORITHMS[category][name]
        if algo is not None:
            return algo['function'], algo['info']
    return None, None


def get_available_algorithms(category):
    """
    Get list of available (implemented) algorithms in a category

    Args:
        category: Algorithm category

    Returns:
        List of algorithm names that are implemented
    """
    if category not in ALGORITHMS:
        return []

    return [name for name, algo in ALGORITHMS[category].items() if algo is not None]


def get_all_algorithms_in_category(category):
    """
    Get all algorithm names in a category (including not yet implemented)

    Args:
        category: Algorithm category

    Returns:
        List of all algorithm names
    """
    if category not in ALGORITHMS:
        return []

    return list(ALGORITHMS[category].keys())
