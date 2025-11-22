"""
DFS (Depth-First Search) Algorithm Implementation
"""


def dfs(arr, target=None):
    """
    Depth-First Search on array represented as binary tree

    Time Complexity: O(n)
    Space Complexity: O(h) where h is height

    Args:
        arr: List of elements (treated as binary tree in array form)
        target: Element to search for (optional)

    Yields:
        Dictionary containing visualization state
    """
    import random

    n = len(arr)
    if n == 0:
        return

    # If no target specified, pick random element
    if target is None:
        target = random.choice(arr) if arr else 0

    visited = []
    stack = [0]  # Start from root (index 0)

    # Initial state
    yield {
        'action': 'start',
        'indices': [],
        'array': arr.copy(),
        'current_pass': 0,
        'target': target,
        'line': 0
    }

    while stack:
        # Pop from stack
        current = stack.pop()

        if current >= n:
            continue

        # Visit current node
        visited.append(current)

        yield {
            'action': 'visit',
            'indices': [current],
            'array': arr.copy(),
            'current_pass': len(visited),
            'target': target,
            'line': 2
        }

        # Check if found
        if arr[current] == target:
            yield {
                'action': 'found',
                'indices': [current],
                'array': arr.copy(),
                'current_pass': len(visited),
                'target': target,
                'line': 3
            }
            break

        # Push right child first (so left is processed first)
        right_child = 2 * current + 2
        if right_child < n:
            stack.append(right_child)

        # Push left child
        left_child = 2 * current + 1
        if left_child < n:
            stack.append(left_child)

    # Complete
    yield {
        'action': 'done',
        'indices': visited,
        'array': arr.copy(),
        'current_pass': len(visited),
        'target': target,
        'line': 5
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'DFS (Depth-First Search)',
        'category': 'Searching',
        'time_complexity': 'O(n)',
        'space_complexity': 'O(h)',
        'description': 'Explores as far as possible along each branch before backtracking. Uses a stack (LIFO).',
        'code': '''def dfs(tree, start):
    visited = []
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            # Add children to stack
            stack.extend(get_children(node))

    return visited'''
    }
