"""
BFS (Breadth-First Search) Algorithm Implementation
"""


def bfs(arr, target=None):
    """
    Breadth-First Search on array represented as binary tree

    Time Complexity: O(n)
    Space Complexity: O(w) where w is max width

    Args:
        arr: List of elements (treated as binary tree in array form)
        target: Element to search for (optional)

    Yields:
        Dictionary containing visualization state
    """
    import random
    from collections import deque

    n = len(arr)
    if n == 0:
        return

    # If no target specified, pick random element
    if target is None:
        target = random.choice(arr) if arr else 0

    visited = []
    queue = deque([0])  # Start from root (index 0)

    # Initial state
    yield {
        'action': 'start',
        'indices': [],
        'array': arr.copy(),
        'current_pass': 0,
        'target': target,
        'line': 0
    }

    while queue:
        # Dequeue from front
        current = queue.popleft()

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

        # Enqueue left child
        left_child = 2 * current + 1
        if left_child < n:
            queue.append(left_child)

        # Enqueue right child
        right_child = 2 * current + 2
        if right_child < n:
            queue.append(right_child)

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
        'name': 'BFS (Breadth-First Search)',
        'category': 'Searching',
        'time_complexity': 'O(n)',
        'space_complexity': 'O(w)',
        'description': 'Explores all nodes at the present depth before moving to nodes at the next depth level. Uses a queue (FIFO).',
        'code': '''def bfs(tree, start):
    visited = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            # Add children to queue
            queue.extend(get_children(node))

    return visited'''
    }
