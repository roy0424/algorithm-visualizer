"""
Quick Sort Algorithm Implementation with Step-by-Step Visualization
"""


def quick_sort(arr):
    """
    Quick Sort Algorithm

    Time Complexity: O(n log n) average, O(n^2) worst
    Space Complexity: O(log n)

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

    # Use iterative quick sort with explicit stack
    stack = [(0, n - 1)]

    while stack:
        low, high = stack.pop()

        if low < high:
            # Highlight the partition being processed
            yield {
                'action': 'partition_start',
                'indices': list(range(low, high + 1)),
                'array': arr.copy(),
                'current_pass': len(stack),
                'line': 2
            }

            # Partition the array
            pivot_index = low
            pivot = arr[high]

            # Highlight pivot
            yield {
                'action': 'pivot',
                'indices': [high],
                'array': arr.copy(),
                'current_pass': len(stack),
                'line': 3
            }

            for j in range(low, high):
                # Compare with pivot
                yield {
                    'action': 'compare',
                    'indices': [j, high],
                    'array': arr.copy(),
                    'current_pass': len(stack),
                    'line': 5
                }

                if arr[j] < pivot:
                    # Swap
                    arr[pivot_index], arr[j] = arr[j], arr[pivot_index]

                    yield {
                        'action': 'swap',
                        'indices': [pivot_index, j],
                        'array': arr.copy(),
                        'current_pass': len(stack),
                        'line': 6
                    }

                    pivot_index += 1

            # Place pivot in correct position
            arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

            yield {
                'action': 'pivot_placed',
                'indices': [pivot_index],
                'array': arr.copy(),
                'current_pass': len(stack),
                'line': 8
            }

            # Push left and right partitions to stack
            stack.append((low, pivot_index - 1))
            stack.append((pivot_index + 1, high))

    # All elements sorted
    yield {
        'action': 'done',
        'indices': list(range(n)),
        'array': arr.copy(),
        'current_pass': 0,
        'line': 10
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Quick Sort',
        'category': 'Sorting',
        'time_complexity': 'O(n log n) avg, O(n²) worst',
        'space_complexity': 'O(log n)',
        'description': 'Selects a pivot element and partitions the array around it, recursively sorting the partitions.',
        'code': '''def quick_sort(arr, low, high):
    if low < high:
        # Partition
        pivot_index = low
        pivot = arr[high]

        for j in range(low, high):
            if arr[j] < pivot:
                arr[pivot_index], arr[j] = arr[j], arr[pivot_index]
                pivot_index += 1

        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

        # Recursively sort partitions
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)

    return arr'''
    }
