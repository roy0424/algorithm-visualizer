"""
2D Grid Breadth-First Search (BFS) - Pathfinding
"""
from collections import deque


def graph_bfs(arr, target=None):
    """
    Breadth-First Search on a 2D grid (pathfinding)

    Time Complexity: O(rows * cols)
    Space Complexity: O(rows * cols)

    Args:
        arr: Array to generate grid from
        target: Not used (for consistency)

    Yields:
        Dictionary containing visualization state
    """
    if not arr:
        return

    # Generate 2D grid from array
    grid, start, end = _generate_grid(arr)

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Initial state
    yield {
        'action': 'start',
        'grid': grid,
        'start': start,
        'end': end,
        'visited': [start],
        'current': None,
        'path': [],
        'stack_queue': {'type': 'queue', 'items': [start]},
        'description': f'Starting BFS from {start} to find {end}',
        'line': 0
    }

    # BFS using queue
    queue = deque([start])
    visited = set([start])
    parent = {}

    while queue:
        yield {
            'action': 'loop',
            'grid': grid,
            'start': start,
            'end': end,
            'visited': list(visited),
            'current': None,
            'path': [],
            'stack_queue': {'type': 'queue', 'items': list(queue)},
            'description': 'BFS iteration',
            'line': 4  # while queue:
        }

        current = queue.popleft()

        yield {
            'action': 'dequeue',
            'grid': grid,
            'start': start,
            'end': end,
            'visited': list(visited),
            'current': current,
            'path': [],
            'stack_queue': {'type': 'queue', 'items': list(queue)},
            'description': f'Dequeue {current}',
            'line': 5  # node = queue.popleft()
        }

        if current == end:
            path = []
            node = end
            while node in parent:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()

            yield {
                'action': 'found',
                'grid': grid,
                'start': start,
                'end': end,
                'visited': list(visited),
                'current': end,
                'path': path,
                'stack_queue': {'type': 'queue', 'items': []},
                'description': f'Path found! Length: {len(path)}',
                'line': 11  # return visited
            }
            return

        row, col = current
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            neighbor = (new_row, new_col)

            if (0 <= new_row < rows and 0 <= new_col < cols and
                grid[new_row][new_col] != 1 and neighbor not in visited):

                visited.add(neighbor)
                parent[neighbor] = current

                yield {
                    'action': 'mark_neighbor',
                    'grid': grid,
                    'start': start,
                    'end': end,
                    'visited': list(visited),
                    'current': neighbor,
                    'path': [],
                    'stack_queue': {'type': 'queue', 'items': list(queue)},
                    'description': f'Mark {neighbor} visited',
                    'line': 8  # visited.add(neighbor)
                }

                queue.append(neighbor)

                yield {
                    'action': 'enqueue',
                    'grid': grid,
                    'start': start,
                    'end': end,
                    'visited': list(visited),
                    'current': neighbor,
                    'path': [],
                    'stack_queue': {'type': 'queue', 'items': list(queue)},
                    'description': f'Enqueue {neighbor}',
                    'line': 9  # queue.append(neighbor)
                }

    # No path found
    yield {
        'action': 'done',
        'grid': grid,
        'start': start,
        'end': end,
        'visited': list(visited),
        'current': None,
        'path': [],
        'stack_queue': {'type': 'queue', 'items': []},
        'description': 'BFS complete. No path found!',
        'line': 4
    }


def _generate_grid(arr):
    """
    Generate a maze with multiple paths using DFS + wall removal

    Args:
        arr: Input array (first element is grid size)

    Returns:
        Tuple of (grid, start, end)
        grid: 2D list where 0 = empty, 1 = wall
        start: (row, col) tuple for starting position
        end: (row, col) tuple for ending position
    """
    import random

    # Extract size from array
    size = arr[0] if arr and arr[0] > 0 else 15

    rows = size
    cols = size

    # Initialize grid with all walls
    grid = [[1 for _ in range(cols)] for _ in range(rows)]

    # Seed for consistent maze generation
    random.seed(42)

    # Maze generation using iterative DFS (avoids recursion limit for large grids)
    def carve_passages_iterative(start_x, start_y, grid):
        """Carve passages from (start_x, start_y) using iterative DFS"""
        stack = [(start_x, start_y)]

        while stack:
            cx, cy = stack[-1]  # Peek at top

            # Get available directions
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            random.shuffle(directions)

            found_unvisited = False
            for dx, dy in directions:
                nx, ny = cx + dx * 2, cy + dy * 2

                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1:
                    # Carve passage
                    grid[cx + dx][cy + dy] = 0
                    grid[nx][ny] = 0
                    stack.append((nx, ny))
                    found_unvisited = True
                    break

            if not found_unvisited:
                stack.pop()  # Backtrack

    # Start carving from (1, 1)
    start = (1, 1)
    grid[start[0]][start[1]] = 0
    carve_passages_iterative(start[0], start[1], grid)

    # Set end point
    end = (rows - 2, cols - 2)
    grid[end[0]][end[1]] = 0

    # Make borders walls
    for i in range(rows):
        grid[i][0] = 1
        grid[i][cols - 1] = 1
    for j in range(cols):
        grid[0][j] = 1
        grid[rows - 1][j] = 1

    # Remove additional walls to create multiple paths (15-20% of existing walls)
    wall_cells = []
    for i in range(2, rows-2):
        for j in range(2, cols-2):
            if grid[i][j] == 1:
                # Check if this wall is between two paths
                neighbors_path = 0
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 0:
                        neighbors_path += 1

                # Only remove walls that are between paths (creates loops)
                if neighbors_path >= 2:
                    wall_cells.append((i, j))

    # Remove 15-20% of removable walls to create multiple paths
    num_to_remove = int(len(wall_cells) * 0.18)
    random.shuffle(wall_cells)
    for i in range(min(num_to_remove, len(wall_cells))):
        r, c = wall_cells[i]
        grid[r][c] = 0

    # Verify path exists using BFS
    def has_path(grid, start, end):
        """Check if path exists from start to end"""
        rows, cols = len(grid), len(grid[0])
        queue = deque([start])
        visited = {start}

        while queue:
            r, c = queue.popleft()
            if (r, c) == end:
                return True

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                    grid[nr][nc] == 0 and (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return False

    # Ensure path exists - if not, carve a direct path
    if not has_path(grid, start, end):
        # Simple carve from start to end
        r, c = start
        while (r, c) != end:
            grid[r][c] = 0
            if r < end[0]:
                r += 1
            elif c < end[1]:
                c += 1
            grid[r][c] = 0

    # Final check: ensure start and end are clear
    grid[start[0]][start[1]] = 0
    grid[end[0]][end[1]] = 0

    return grid, start, end


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Graph BFS',
        'category': 'Graph Algorithms',
        'time_complexity': 'O(V + E)',
        'space_complexity': 'O(V)',
        'description': 'Breadth-first search traversal of a graph using a queue.',
        'code': '''def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited'''
    }
