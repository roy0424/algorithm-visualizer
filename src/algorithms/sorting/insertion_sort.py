"""
Insertion Sort Algorithm Implementation with Step-by-Step Visualization
"""


def insertion_sort(arr):
    """
    Insertion Sort Algorithm

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

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        # Mark the key being inserted
        yield {
            'action': 'mark_key',
            'indices': [i],
            'array': arr.copy(),
            'current_pass': i,
            'line': 2
        }

        # Move elements greater than key one position ahead
        while j >= 0 and arr[j] > key:
            # Compare
            yield {
                'action': 'compare',
                'indices': [j, j + 1],
                'array': arr.copy(),
                'current_pass': i,
                'line': 4
            }

            arr[j + 1] = arr[j]

            # Shift
            yield {
                'action': 'shift',
                'indices': [j, j + 1],
                'array': arr.copy(),
                'current_pass': i,
                'line': 5
            }

            j -= 1

        # Insert key at correct position
        arr[j + 1] = key

        yield {
            'action': 'insert',
            'indices': [j + 1],
            'array': arr.copy(),
            'current_pass': i,
            'line': 7
        }

    # All elements sorted
    yield {
        'action': 'done',
        'indices': list(range(n)),
        'array': arr.copy(),
        'current_pass': n,
        'line': 9
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Insertion Sort',
        'category': 'Sorting',
        'time_complexity': 'O(n²)',
        'space_complexity': 'O(1)',
        'description': 'Builds the final sorted array one item at a time by inserting each element into its correct position.',
        'code': '''def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr'''
    }
