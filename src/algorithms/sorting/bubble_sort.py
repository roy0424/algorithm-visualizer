"""
Bubble Sort Algorithm Implementation with Step-by-Step Visualization
"""


def bubble_sort(arr):
    """
    Bubble Sort Algorithm

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    Args:
        arr: List of comparable elements

    Yields:
        Dictionary containing:
        - action: Type of action ('compare', 'swap', 'done')
        - indices: Indices being compared/swapped
        - array: Current state of array
        - current_pass: Current pass number
        - line: Line number for code highlighting
    """
    n = len(arr)

    # Initial state
    yield {
        'action': 'start',
        'indices': [],
        'array': arr.copy(),
        'current_pass': 0,
        'line': 0  # def bubble_sort(arr):
    }

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            # Comparing two elements
            yield {
                'action': 'compare',
                'indices': [j, j + 1],
                'array': arr.copy(),
                'current_pass': i + 1,
                'line': 4  # for j in range(0, n - i - 1):
            }

            if arr[j] > arr[j + 1]:
                # Swap elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

                yield {
                    'action': 'swap',
                    'indices': [j, j + 1],
                    'array': arr.copy(),
                    'current_pass': i + 1,
                    'line': 5  # if arr[j] > arr[j + 1]:
                }

        # Mark sorted element
        yield {
            'action': 'sorted',
            'indices': [n - i - 1],
            'array': arr.copy(),
            'current_pass': i + 1,
            'line': 7  # swapped = True
        }

        # Early termination if no swaps occurred
        if not swapped:
            break

    # All elements sorted
    yield {
        'action': 'done',
        'indices': list(range(n)),
        'array': arr.copy(),
        'current_pass': i + 1,
        'line': 9  # return arr
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Bubble Sort',
        'category': 'Sorting',
        'time_complexity': 'O(n²)',
        'space_complexity': 'O(1)',
        'description': 'Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.',
        'code': '''def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr'''
    }
