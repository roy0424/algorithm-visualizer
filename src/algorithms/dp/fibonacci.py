"""
Fibonacci Sequence using Dynamic Programming
"""


def fibonacci(arr, target=None):
    """
    Fibonacci Sequence with DP Tabulation

    Time Complexity: O(n)
    Space Complexity: O(n)

    Args:
        arr: Not used (for interface compatibility)
        target: Which fibonacci number to compute (default: 10)

    Yields:
        Dictionary containing visualization state
    """
    n = target if target is not None else 10
    n = max(2, min(n, 20))  # Limit between 2 and 20

    # Initialize DP table
    dp = [[None] * 2 for _ in range(n + 1)]
    dp[0][0] = 0
    dp[1][0] = 1

    # Initial state
    yield {
        'action': 'start',
        'indices': [],
        'array': arr.copy() if arr else [],
        'dp_table': [row[:] for row in dp],
        'current_cell': None,
        'problem': 'Fibonacci',
        'description': f'Computing Fibonacci({n})',
        'line': 0
    }

    # Compute fibonacci numbers
    for i in range(2, n + 1):
        # Show current cell being computed
        yield {
            'action': 'compute',
            'indices': [],
            'array': arr.copy() if arr else [],
            'dp_table': [row[:] for row in dp],
            'current_cell': (i, 0),
            'problem': 'Fibonacci',
            'description': f'Computing F({i}) = F({i-1}) + F({i-2})',
            'line': 2
        }

        dp[i][0] = dp[i-1][0] + dp[i-2][0]

        # Show computed value
        yield {
            'action': 'computed',
            'indices': [],
            'array': arr.copy() if arr else [],
            'dp_table': [row[:] for row in dp],
            'current_cell': (i, 0),
            'problem': 'Fibonacci',
            'description': f'F({i}) = {dp[i][0]}',
            'line': 3
        }

    # Done
    yield {
        'action': 'done',
        'indices': [],
        'array': arr.copy() if arr else [],
        'dp_table': [row[:] for row in dp],
        'current_cell': (n, 0),
        'problem': 'Fibonacci',
        'description': f'Result: Fibonacci({n}) = {dp[n][0]}',
        'line': 4
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Fibonacci',
        'category': 'Dynamic Programming',
        'time_complexity': 'O(n)',
        'space_complexity': 'O(n)',
        'description': 'Computes Fibonacci sequence using bottom-up DP approach (tabulation).',
        'code': '''def fibonacci(n):
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1

    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]'''
    }
