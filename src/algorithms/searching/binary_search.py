"""
Binary Search Algorithm Implementation with Step-by-Step Visualization
"""


def binary_search(arr, target=None):
    """
    Binary Search Algorithm (requires sorted array)

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        arr: List of comparable elements (will be sorted)
        target: Element to search for (if None, picks from original array)

    Yields:
        Dictionary containing visualization state
    """
    import random

    # If no target specified, pick a random element from the ORIGINAL array
    if target is None:
        target = random.choice(arr) if arr else 0

    # Now sort the array for binary search
    sorted_arr = sorted(arr)
    n = len(sorted_arr)

    # Initial state - show sorted array
    yield {
        'action': 'start',
        'indices': [],
        'array': sorted_arr.copy(),
        'current_pass': 0,
        'target': target,
        'line': 1
    }

    left = 0
    right = n - 1
    found_index = -1

    while left <= right:
        mid = (left + right) // 2

        # Highlight search range
        yield {
            'action': 'range',
            'indices': list(range(left, right + 1)),
            'array': sorted_arr.copy(),
            'current_pass': 0,
            'target': target,
            'line': 3
        }

        # Check middle element
        yield {
            'action': 'compare',
            'indices': [mid],
            'array': sorted_arr.copy(),
            'current_pass': 0,
            'target': target,
            'line': 4
        }

        if sorted_arr[mid] == target:
            found_index = mid
            # Found the target
            yield {
                'action': 'found',
                'indices': [mid],
                'array': sorted_arr.copy(),
                'current_pass': 0,
                'target': target,
                'line': 5
            }
            break
        elif sorted_arr[mid] < target:
            # Target is in right half
            left = mid + 1
            yield {
                'action': 'search_right',
                'indices': [mid],
                'array': sorted_arr.copy(),
                'current_pass': 0,
                'target': target,
                'line': 6
            }
        else:
            # Target is in left half
            right = mid - 1
            yield {
                'action': 'search_left',
                'indices': [mid],
                'array': sorted_arr.copy(),
                'current_pass': 0,
                'target': target,
                'line': 8
            }

    if found_index == -1:
        # Target not found
        yield {
            'action': 'not_found',
            'indices': [],
            'array': sorted_arr.copy(),
            'current_pass': 0,
            'target': target,
            'line': 10
        }
    else:
        # Complete
        yield {
            'action': 'done',
            'indices': [found_index],
            'array': sorted_arr.copy(),
            'current_pass': 0,
            'target': target,
            'line': 11
        }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Binary Search',
        'category': 'Searching',
        'time_complexity': 'O(log n)',
        'space_complexity': 'O(1)',
        'description': 'Efficiently searches a sorted array by repeatedly dividing the search interval in half.',
        'code': '''def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1'''
    }
