"""
A* Pathfinding Algorithm
"""
import heapq


def astar(arr, target=None):
    """
    A* algorithm for finding shortest path to a goal node

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)

    Args:
        arr: Array to generate graph from
        target: Target/goal node (optional, uses last node if not specified)

    Yields:
        Dictionary containing visualization state
    """
    if not arr:
        return

    # Generate graph from array
    nodes, edges, adj_list = _generate_graph(arr)

    if not nodes:
        return

    start_node = nodes[0]
    goal_node = nodes[-1] if target is None else (target if target in nodes else nodes[-1])

    # Initialize g_score (actual cost from start)
    g_score = {node: float('inf') for node in nodes}
    g_score[start_node] = 0

    # Initialize f_score (g_score + heuristic)
    f_score = {node: float('inf') for node in nodes}
    f_score[start_node] = _heuristic(start_node, goal_node)

    # Priority queue: (f_score, node)
    pq = [(f_score[start_node], start_node)]
    visited = set()
    path_edges = set()
    parent = {}

    # Initial state
    yield {
        'action': 'start',
        'nodes': nodes,
        'edges': edges,
        'visited': [],
        'current_node': None,
        'highlighted_edges': [],
        'path_edges': [],
        'distances': {node: f"g={g_score[node]:.1f}, f={f_score[node]:.1f}" for node in nodes},
        'description': f'Starting A* from node {start_node} to goal {goal_node}',
        'line': 0
    }

    while pq:
        current_f, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        # Show current node being processed
        yield {
            'action': 'visit',
            'nodes': nodes,
            'edges': edges,
            'visited': list(visited),
            'current_node': current,
            'highlighted_edges': [],
            'path_edges': list(path_edges),
            'distances': {node: f"g={g_score[node]:.1f}, f={f_score[node]:.1f}" for node in nodes},
            'description': f'Processing node {current} with f={current_f:.1f}, g={g_score[current]:.1f}',
            'line': 1
        }

        # Check if we reached the goal
        if current == goal_node:
            # Reconstruct path
            final_path = []
            node = goal_node
            while node in parent:
                final_path.append((parent[node], node))
                node = parent[node]

            yield {
                'action': 'done',
                'nodes': nodes,
                'edges': edges,
                'visited': list(visited),
                'current_node': goal_node,
                'highlighted_edges': [],
                'path_edges': final_path,
                'distances': {node: f"g={g_score[node]:.1f}, f={f_score[node]:.1f}" for node in nodes},
                'description': f'Goal {goal_node} reached! Path cost: {g_score[goal_node]:.1f}',
                'line': 5
            }
            return

        # Check neighbors
        for neighbor, weight in adj_list.get(current, []):
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + weight

            # Highlight edge being considered
            yield {
                'action': 'relax',
                'nodes': nodes,
                'edges': edges,
                'visited': list(visited),
                'current_node': current,
                'highlighted_edges': [(current, neighbor)],
                'path_edges': list(path_edges),
                'distances': {node: f"g={g_score[node]:.1f}, f={f_score[node]:.1f}" for node in nodes},
                'description': f'Checking edge ({current}, {neighbor}): g={g_score[current]:.1f} + {weight} = {tentative_g:.1f} vs {g_score[neighbor]:.1f}',
                'line': 2
            }

            # Update if better path found
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + _heuristic(neighbor, goal_node)
                parent[neighbor] = current
                heapq.heappush(pq, (f_score[neighbor], neighbor))

                # Update path edges
                if neighbor in parent:
                    # Remove old edge to this neighbor
                    path_edges = {e for e in path_edges if e[1] != neighbor and e[0] != neighbor}
                    # Add new edge
                    path_edges.add((current, neighbor))

                yield {
                    'action': 'update',
                    'nodes': nodes,
                    'edges': edges,
                    'visited': list(visited),
                    'current_node': current,
                    'highlighted_edges': [(current, neighbor)],
                    'path_edges': list(path_edges),
                    'distances': {node: f"g={g_score[node]:.1f}, f={f_score[node]:.1f}" for node in nodes},
                    'description': f'Updated node {neighbor}: g={g_score[neighbor]:.1f}, h={_heuristic(neighbor, goal_node):.1f}, f={f_score[neighbor]:.1f}',
                    'line': 3
                }

    # If we get here, no path was found
    yield {
        'action': 'done',
        'nodes': nodes,
        'edges': edges,
        'visited': list(visited),
        'current_node': None,
        'highlighted_edges': [],
        'path_edges': list(path_edges),
        'distances': {node: f"g={g_score[node]:.1f}, f={f_score[node]:.1f}" for node in nodes},
        'description': f'A* complete. No path to goal {goal_node}',
        'line': 5
    }


def _heuristic(node, goal):
    """
    Heuristic function for A* (estimated cost to goal)
    Uses absolute difference between node values (admissible heuristic)

    Args:
        node: Current node
        goal: Goal node

    Returns:
        Estimated cost from node to goal
    """
    # Use absolute difference as heuristic (admissible for this graph)
    return abs(node - goal) * 0.5


def _generate_graph(arr):
    """
    Generate a tree from an array

    Args:
        arr: Input array

    Returns:
        Tuple of (nodes, edges, adjacency_list)
    """
    # Get unique nodes (limit to 10 for visualization)
    nodes = sorted(list(set(arr)))[:10]

    if len(nodes) < 2:
        return nodes, [], {}

    # Generate tree structure
    edges = []
    adj_list = {node: [] for node in nodes}

    # Create a balanced tree structure
    # First node is root, others are added as children in a breadth-first manner
    root = nodes[0]

    # For each node (except root), connect it to a parent
    for i in range(1, len(nodes)):
        # Parent is at index (i-1)//2 (binary tree structure)
        parent_idx = (i - 1) // 2
        parent = nodes[parent_idx]
        child = nodes[i]

        weight = abs(parent - child) % 10 + 1

        # Add edge (undirected for visualization)
        edges.append((parent, child, weight))
        adj_list[parent].append((child, weight))
        adj_list[child].append((parent, weight))

    return nodes, edges, adj_list


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': "A* Algorithm",
        'category': 'Graph Algorithms',
        'time_complexity': 'O((V + E) log V)',
        'space_complexity': 'O(V)',
        'description': 'Finds the shortest path from start to goal using heuristic-guided search (f = g + h).',
        'code': '''def astar(graph, start, goal, heuristic):
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    pq = [(f_score[start], start)]
    visited = set()

    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            return reconstruct_path(current)
        visited.add(current)

        for neighbor, weight in graph[current]:
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_score[neighbor], neighbor))

    return None'''
    }
