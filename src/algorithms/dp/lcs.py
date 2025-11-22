"""
Longest Common Subsequence using Dynamic Programming
"""


def lcs(arr, target=None):
    """
    Longest Common Subsequence

    Time Complexity: O(m * n)
    Space Complexity: O(m * n)

    Args:
        arr: First sequence
        target: Second sequence (if None, generates one)

    Yields:
        Dictionary containing visualization state
    """
    if not arr:
        return

    # Create two sequences from the array
    mid = len(arr) // 2
    seq1 = arr[:mid] if mid > 0 else arr
    seq2 = arr[mid:] if mid > 0 else [x + 1 for x in arr[:3]]  # Offset values

    if not seq1 or not seq2:
        seq1 = arr[:5] if len(arr) >= 5 else arr
        seq2 = [arr[i] if i < len(arr) else i for i in range(5)]

    m, n = len(seq1), len(seq2)
    m, n = min(m, 10), min(n, 10)  # Limit size
    seq1, seq2 = seq1[:m], seq2[:n]

    # Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initial state
    yield {
        'action': 'start',
        'indices': [],
        'array': arr.copy(),
        'dp_table': [row[:] for row in dp],
        'current_cell': None,
        'problem': 'LCS',
        'description': f'LCS of {seq1} and {seq2}',
        'line': 0
    }

    # Build table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Show current cell
            yield {
                'action': 'compute',
                'indices': [i-1, m+j-1] if m+j-1 < len(arr) else [i-1],
                'array': arr.copy(),
                'dp_table': [row[:] for row in dp],
                'current_cell': (i, j),
                'problem': 'LCS',
                'description': f'Comparing seq1[{i-1}]={seq1[i-1]} with seq2[{j-1}]={seq2[j-1]}',
                'line': 2
            }

            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                desc = f'Match! dp[{i}][{j}] = {dp[i][j]}'
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                desc = f'No match. dp[{i}][{j}] = max({dp[i-1][j]}, {dp[i][j-1]}) = {dp[i][j]}'

            # Show computed value
            yield {
                'action': 'computed',
                'indices': [],
                'array': arr.copy(),
                'dp_table': [row[:] for row in dp],
                'current_cell': (i, j),
                'problem': 'LCS',
                'description': desc,
                'line': 3
            }

    # Done
    yield {
        'action': 'done',
        'indices': [],
        'array': arr.copy(),
        'dp_table': [row[:] for row in dp],
        'current_cell': (m, n),
        'problem': 'LCS',
        'description': f'LCS length: {dp[m][n]}',
        'line': 5
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Longest Common Subsequence',
        'category': 'Dynamic Programming',
        'time_complexity': 'O(m × n)',
        'space_complexity': 'O(m × n)',
        'description': 'Finds the longest subsequence common to two sequences.',
        'code': '''def lcs(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]'''
    }
