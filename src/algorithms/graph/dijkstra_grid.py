"""
Dijkstra's Shortest Path Algorithm on 2D Grid
"""
import heapq
from algorithms.graph.graph_dfs import _generate_grid


def dijkstra_grid(arr, target=None):
    """
    Dijkstra's algorithm for finding shortest path in a 2D grid

    Time Complexity: O(V log V) where V is number of cells
    Space Complexity: O(V)

    Args:
        arr: Array containing grid size [size] (e.g., [20] for 20x20)
        target: Not used, but kept for interface compatibility

    Yields:
        Dictionary containing visualization state
    """
    if not arr:
        return

    # Generate grid using same method as DFS/BFS (seed=42 for consistency)
    grid, start, end = _generate_grid(arr)

    if not grid or not start or not end:
        return

    rows = len(grid)
    cols = len(grid[0])

    # Initialize distances
    distances = {}
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:  # Not a wall
                distances[(i, j)] = float('inf')

    distances[start] = 0

    # Priority queue: (distance, position)
    pq = [(0, start)]
    visited = set()
    parent = {}
    visit_order = {}
    visit_counter = 0

    # Initial state
    yield {
        'action': 'start',
        'grid': grid,
        'start': start,
        'end': end,
        'visited': [],
        'current': None,
        'path': [],
        'visit_order': {},
        'description': f"Dijkstra: Starting from {start} to {end}",
        'stats': {'nodes_visited': 0, 'path_length': 0, 'steps': 0},
        'step': 0,
        'line': 0
    }

    step = 0

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        visit_counter += 1
        visit_order[current] = visit_counter
        step += 1

        # Show current node being processed
        yield {
            'action': 'visit',
            'grid': grid,
            'start': start,
            'end': end,
            'visited': list(visited),
            'current': current,
            'path': [],
            'visit_order': visit_order.copy(),
            'description': f"Dijkstra: Visiting {current} (distance: {current_dist:.1f})",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step
            },
            'step': step,
            'line': 1
        }

        # Check if we reached the goal
        if current == end:
            # Reconstruct path
            path = []
            node = end
            while node in parent:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()

            yield {
                'action': 'done',
                'grid': grid,
                'start': start,
                'end': end,
                'visited': list(visited),
                'current': end,
                'path': path,
                'visit_order': visit_order.copy(),
                'description': f"Dijkstra: Goal reached! Path length: {len(path)}, Nodes visited: {len(visited)}",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': len(path),
                    'steps': step
                },
                'step': step,
                'line': 5
            }
            return

        # Check neighbors (up, down, left, right)
        row, col = current
        neighbors = [
            (row - 1, col),  # Up
            (row + 1, col),  # Down
            (row, col - 1),  # Left
            (row, col + 1),  # Right
        ]

        for neighbor in neighbors:
            n_row, n_col = neighbor

            # Check bounds
            if not (0 <= n_row < rows and 0 <= n_col < cols):
                continue

            # Check if wall or visited
            if grid[n_row][n_col] == 1 or neighbor in visited:
                continue

            # Calculate new distance (uniform cost of 1 per move)
            new_dist = distances[current] + 1

            # Relax edge if shorter path found
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    # No path found
    yield {
        'action': 'done',
        'grid': grid,
        'start': start,
        'end': end,
        'visited': list(visited),
        'current': None,
        'path': [],
        'visit_order': visit_order.copy(),
        'description': f"Dijkstra: No path found. Nodes visited: {len(visited)}",
        'stats': {
            'nodes_visited': len(visited),
            'path_length': 0,
            'steps': step
        },
        'step': step,
        'line': 5
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': "Dijkstra's Algorithm",
        'category': 'Graph Algorithms',
        'time_complexity': 'O(V log V)',
        'space_complexity': 'O(V)',
        'description': 'Finds shortest path in a grid. Explores uniformly in all directions.',
        'code': '''def dijkstra_grid(grid, start, end):
    distances = {start: 0}
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return reconstruct_path(parent, end)

        for neighbor in get_neighbors(current):
            new_dist = distances[current] + 1
            if new_dist < distances.get(neighbor, inf):
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return None'''
    }
