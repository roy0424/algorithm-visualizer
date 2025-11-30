"""
A* Pathfinding Algorithm on 2D Grid
"""
import heapq
from algorithms.graph.graph_dfs import _generate_grid


def astar_grid(arr, target=None):
    """
    A* algorithm for finding shortest path in a 2D grid

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

    # Initialize g_score (actual cost from start)
    g_score = {}
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:  # Not a wall
                g_score[(i, j)] = float('inf')

    g_score[start] = 0

    # Initialize f_score (g_score + heuristic)
    f_score = {}
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                f_score[(i, j)] = float('inf')

    f_score[start] = _manhattan_distance(start, end)

    # Priority queue: (f_score, position)
    pq = [(f_score[start], start)]
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
        'description': f"A*: Starting from {start} to {end} (using Manhattan distance heuristic)",
        'stats': {'nodes_visited': 0, 'path_length': 0, 'steps': 0},
        'step': 0,
        'line': 0
    }

    step = 0

    while pq:
        current_f, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        visit_counter += 1
        visit_order[current] = visit_counter
        step += 1

        # Show current node being processed
        h_value = _manhattan_distance(current, end)
        g_value = g_score[current]

        yield {
            'action': 'visit',
            'grid': grid,
            'start': start,
            'end': end,
            'visited': list(visited),
            'current': current,
            'path': [],
            'visit_order': visit_order.copy(),
            'description': f"A*: Visiting {current} (g={g_value:.0f}, h={h_value:.0f}, f={current_f:.0f})",
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
                'description': f"A*: Goal reached! Path length: {len(path)}, Nodes visited: {len(visited)} ⭐",
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

            # Calculate tentative g_score (uniform cost of 1 per move)
            tentative_g = g_score[current] + 1

            # Update if better path found
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                h = _manhattan_distance(neighbor, end)
                f_score[neighbor] = tentative_g + h
                parent[neighbor] = current
                heapq.heappush(pq, (f_score[neighbor], neighbor))

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
        'description': f"A*: No path found. Nodes visited: {len(visited)}",
        'stats': {
            'nodes_visited': len(visited),
            'path_length': 0,
            'steps': step
        },
        'step': step,
        'line': 5
    }


def _manhattan_distance(pos1, pos2):
    """
    Calculate Manhattan distance between two positions

    Args:
        pos1: (row, col) tuple
        pos2: (row, col) tuple

    Returns:
        Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': "A* Algorithm",
        'category': 'Graph Algorithms',
        'time_complexity': 'O(V log V)',
        'space_complexity': 'O(V)',
        'description': 'Finds shortest path using heuristic (f=g+h). More efficient than Dijkstra!',
        'code': '''def astar_grid(grid, start, end):
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    pq = [(f_score[start], start)]
    visited = set()

    while pq:
        _, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return reconstruct_path(parent, end)

        for neighbor in get_neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, inf):
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                heapq.heappush(pq, (f_score[neighbor], neighbor))

    return None'''
    }
