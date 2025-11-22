"""
Merge Sort Algorithm Implementation with Step-by-Step Visualization
"""


def merge_sort(arr):
    """
    Merge Sort Algorithm

    Time Complexity: O(n log n)
    Space Complexity: O(n)

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

    # Use iterative merge sort for easier visualization
    current_size = 1

    while current_size < n:
        left_start = 0

        while left_start < n:
            # Find ending point of left subarray
            mid = min(left_start + current_size - 1, n - 1)
            # Find ending point of right subarray
            right_end = min(left_start + current_size * 2 - 1, n - 1)

            if mid < right_end:
                # Highlight the subarrays being merged
                yield {
                    'action': 'divide',
                    'indices': list(range(left_start, right_end + 1)),
                    'array': arr.copy(),
                    'current_pass': current_size,
                    'line': 3
                }

                # Merge
                yield from merge(arr, left_start, mid, right_end)

            left_start += current_size * 2

        current_size *= 2

    # All elements sorted
    yield {
        'action': 'done',
        'indices': list(range(n)),
        'array': arr.copy(),
        'current_pass': current_size,
        'line': 10
    }


def merge(arr, left, mid, right):
    """Merge two sorted subarrays"""
    # Create temp arrays
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]

    i = j = 0
    k = left

    # Merge the temp arrays back
    while i < len(left_arr) and j < len(right_arr):
        # Compare elements
        yield {
            'action': 'compare',
            'indices': [left + i, mid + 1 + j],
            'array': arr.copy(),
            'current_pass': 0,
            'line': 5
        }

        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1

        # Show merge progress
        yield {
            'action': 'merge',
            'indices': [k],
            'array': arr.copy(),
            'current_pass': 0,
            'line': 7
        }

        k += 1

    # Copy remaining elements
    while i < len(left_arr):
        arr[k] = left_arr[i]
        yield {
            'action': 'merge',
            'indices': [k],
            'array': arr.copy(),
            'current_pass': 0,
            'line': 8
        }
        i += 1
        k += 1

    while j < len(right_arr):
        arr[k] = right_arr[j]
        yield {
            'action': 'merge',
            'indices': [k],
            'array': arr.copy(),
            'current_pass': 0,
            'line': 9
        }
        j += 1
        k += 1


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Merge Sort',
        'category': 'Sorting',
        'time_complexity': 'O(n log n)',
        'space_complexity': 'O(n)',
        'description': 'Divide and conquer algorithm that divides array into halves, sorts them, and merges them back.',
        'code': '''def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result'''
    }
