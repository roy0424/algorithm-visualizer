"""
Selection Sort Algorithm Implementation with Step-by-Step Visualization
"""


def selection_sort(arr):
    """
    Selection Sort Algorithm

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    Args:
        arr: List of comparable elements

    Yields:
        Dictionary containing visualization state
    """
    n = len(arr)

    # Initial state
    yield {
        'action': 'start',
        'indices': [],
        'array': arr.copy(),
        'current_pass': 0,
        'line': 1
    }

    for i in range(n):
        min_idx = i

        # Mark current position
        yield {
            'action': 'mark_position',
            'indices': [i],
            'array': arr.copy(),
            'current_pass': i + 1,
            'line': 2
        }

        for j in range(i + 1, n):
            # Comparing to find minimum
            yield {
                'action': 'compare',
                'indices': [min_idx, j],
                'array': arr.copy(),
                'current_pass': i + 1,
                'line': 4
            }

            if arr[j] < arr[min_idx]:
                min_idx = j

        # Swap if needed
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

            yield {
                'action': 'swap',
                'indices': [i, min_idx],
                'array': arr.copy(),
                'current_pass': i + 1,
                'line': 6
            }

        # Mark as sorted
        yield {
            'action': 'sorted',
            'indices': [i],
            'array': arr.copy(),
            'current_pass': i + 1,
            'line': 8
        }

    # All elements sorted
    yield {
        'action': 'done',
        'indices': list(range(n)),
        'array': arr.copy(),
        'current_pass': n,
        'line': 10
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Selection Sort',
        'category': 'Sorting',
        'time_complexity': 'O(n²)',
        'space_complexity': 'O(1)',
        'description': 'Divides the list into sorted and unsorted regions, repeatedly selecting the smallest element from the unsorted region.',
        'code': '''def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr'''
    }
