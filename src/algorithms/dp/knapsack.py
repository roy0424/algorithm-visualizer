"""
0/1 Knapsack Problem using Dynamic Programming
"""


def knapsack(arr, capacity=None):
    """
    0/1 Knapsack Problem

    Time Complexity: O(n * W)
    Space Complexity: O(n * W)

    Args:
        arr: List of item values
        capacity: Knapsack capacity (default: sum(arr)//2)

    Yields:
        Dictionary containing visualization state
    """
    if not arr:
        return

    n = len(arr)
    weights = arr  # Use array values as weights
    values = arr   # Use array values as values too
    W = capacity if capacity is not None else sum(arr) // 2
    W = max(1, min(W, 50))  # Limit capacity

    # Initialize DP table
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Initial state
    yield {
        'action': 'start',
        'indices': [],
        'array': arr.copy(),
        'dp_table': [row[:] for row in dp],
        'current_cell': None,
        'problem': 'Knapsack',
        'description': f'0/1 Knapsack: {n} items, capacity {W}',
        'line': 0
    }

    # Build table
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            # Show current cell
            yield {
                'action': 'compute',
                'indices': [i-1],
                'array': arr.copy(),
                'dp_table': [row[:] for row in dp],
                'current_cell': (i, w),
                'problem': 'Knapsack',
                'description': f'Item {i-1} (weight={weights[i-1]}, value={values[i-1]}), capacity={w}',
                'line': 2
            }

            if weights[i-1] <= w:
                # Can include this item
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                # Cannot include
                dp[i][w] = dp[i-1][w]

            # Show computed value
            yield {
                'action': 'computed',
                'indices': [i-1],
                'array': arr.copy(),
                'dp_table': [row[:] for row in dp],
                'current_cell': (i, w),
                'problem': 'Knapsack',
                'description': f'dp[{i}][{w}] = {dp[i][w]}',
                'line': 3
            }

    # Done
    yield {
        'action': 'done',
        'indices': [],
        'array': arr.copy(),
        'dp_table': [row[:] for row in dp],
        'current_cell': (n, W),
        'problem': 'Knapsack',
        'description': f'Maximum value: {dp[n][W]}',
        'line': 5
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Knapsack Problem',
        'category': 'Dynamic Programming',
        'time_complexity': 'O(n × W)',
        'space_complexity': 'O(n × W)',
        'description': '0/1 Knapsack: Find the maximum value subset of items that fit in a knapsack of given capacity.',
        'code': '''def knapsack(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][W]'''
    }
