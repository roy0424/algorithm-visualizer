"""
Heap Sort Algorithm Implementation with Step-by-Step Visualization
"""


def heap_sort(arr):
    """
    Heap Sort Algorithm

    Time Complexity: O(n log n)
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
        'line': 0
    }

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i, 'build')

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]

        yield {
            'action': 'swap',
            'indices': [0, i],
            'array': arr.copy(),
            'current_pass': n - i,
            'line': 3
        }

        # Mark as sorted
        yield {
            'action': 'sorted',
            'indices': [i],
            'array': arr.copy(),
            'current_pass': n - i,
            'line': 4
        }

        # Heapify the reduced heap
        yield from heapify(arr, i, 0, 'extract')

    # All elements sorted
    yield {
        'action': 'done',
        'indices': list(range(n)),
        'array': arr.copy(),
        'current_pass': n,
        'line': 7
    }


def heapify(arr, n, i, phase):
    """Helper function to heapify a subtree rooted at index i"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Highlight current node and children
    indices_to_check = [i]
    if left < n:
        indices_to_check.append(left)
    if right < n:
        indices_to_check.append(right)

    yield {
        'action': 'heapify_check',
        'indices': indices_to_check,
        'array': arr.copy(),
        'current_pass': 0,
        'line': 1
    }

    # Check if left child is larger than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child is larger than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        yield {
            'action': 'heapify_swap',
            'indices': [i, largest],
            'array': arr.copy(),
            'current_pass': 0,
            'line': 2
        }

        # Recursively heapify the affected sub-tree
        yield from heapify(arr, n, largest, phase)


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Heap Sort',
        'category': 'Sorting',
        'time_complexity': 'O(n log n)',
        'space_complexity': 'O(1)',
        'description': 'Uses a binary heap data structure to sort elements. Builds a max heap then repeatedly extracts the maximum.',
        'code': '''def heap_sort(arr):
    n = len(arr)
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr'''
    }
