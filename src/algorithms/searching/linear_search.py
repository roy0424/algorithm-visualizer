"""
Linear Search Algorithm Implementation with Step-by-Step Visualization
"""


def linear_search(arr, target=None):
    """
    Linear Search Algorithm

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        arr: List of comparable elements
        target: Element to search for (if None, picks a random element from array)

    Yields:
        Dictionary containing visualization state
    """
    import random
    n = len(arr)

    # If no target specified, pick a random element from the array
    if target is None:
        target = random.choice(arr) if arr else 0

    # Initial state
    yield {
        'action': 'start',
        'indices': [],
        'array': arr.copy(),
        'current_pass': 0,
        'target': target,
        'line': 1
    }

    found_index = -1

    for i in range(n):
        # Compare current element with target
        yield {
            'action': 'compare',
            'indices': [i],
            'array': arr.copy(),
            'current_pass': i + 1,
            'target': target,
            'line': 3
        }

        if arr[i] == target:
            found_index = i
            # Found the target
            yield {
                'action': 'found',
                'indices': [i],
                'array': arr.copy(),
                'current_pass': i + 1,
                'target': target,
                'line': 4
            }
            break

    if found_index == -1:
        # Target not found
        yield {
            'action': 'not_found',
            'indices': [],
            'array': arr.copy(),
            'current_pass': n,
            'target': target,
            'line': 6
        }
    else:
        # Complete
        yield {
            'action': 'done',
            'indices': [found_index],
            'array': arr.copy(),
            'current_pass': n,
            'target': target,
            'line': 7
        }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Linear Search',
        'category': 'Searching',
        'time_complexity': 'O(n)',
        'space_complexity': 'O(1)',
        'description': 'Sequentially checks each element until the target is found or the end is reached.',
        'code': '''def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1'''
    }
