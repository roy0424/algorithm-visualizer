"""
A* Pathfinding Algorithm on Weighted Graph
"""
import heapq
from algorithms.graph.dijkstra_weighted import _generate_weighted_graph


def astar_weighted(arr, target=None):
    """
    A* algorithm for finding shortest path in a weighted graph

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)

    Args:
        arr: Array to generate graph from
        target: Not used, but kept for interface compatibility

    Yields:
        Dictionary containing visualization state
    """
    if not arr:
        return

    # Generate weighted graph (same as Dijkstra)
    nodes, edges, adj_list, start, goal = _generate_weighted_graph(arr)

    if not nodes:
        return

    # Initialize g_score (actual cost from start)
    g_score = {node: float('inf') for node in nodes}
    g_score[start] = 0

    # Initialize f_score (g_score + heuristic)
    f_score = {node: float('inf') for node in nodes}
    f_score[start] = _heuristic(start, goal, nodes)

    # Priority queue: (f_score, node)
    pq = [(f_score[start], start)]
    visited = set()
    parent = {}
    path_edges = set()

    # Initial state
    yield {
        'action': 'start',
        'nodes': nodes,
        'edges': edges,
        'start': start,
        'end': goal,
        'visited': [],
        'current': None,
        'highlighted_edges': [],
        'path': [],
        'description': f"A*: Starting from node {start} to {goal} (with heuristic)",
        'stats': {'nodes_visited': 0, 'path_length': 0, 'steps': 0, 'total_cost': 0},
        'step': 0,
        'line': 0
    }

    step = 0

    while pq:
        current_f, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        step += 1

        # Show current node being processed
        h_value = _heuristic(current, goal, nodes)
        g_value = g_score[current]

        yield {
            'action': 'visit',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"A*: Visiting node {current} (g={g_value:.0f}, h={h_value:.0f}, f={current_f:.0f})",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': int(g_value)
            },
            'step': step,
            'line': 1
        }

        # Check if we reached the goal
        if current == goal:
            # Reconstruct path
            path = []
            node = goal
            while node in parent:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()

            # Calculate path edges
            path_edges = []
            for i in range(len(path) - 1):
                path_edges.append((path[i], path[i+1]))

            yield {
                'action': 'done',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': goal,
                'highlighted_edges': path_edges,
                'path': path,
                'description': f"A*: Goal reached! Cost: {int(g_score[goal])}, Nodes visited: {len(visited)} ⭐",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': len(path),
                    'steps': step,
                    'total_cost': int(g_score[goal])
                },
                'step': step,
                'line': 5
            }
            return

        # Check neighbors
        for neighbor, weight in adj_list.get(current, []):
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + weight

            # Highlight edge being considered
            h = _heuristic(neighbor, goal, nodes)
            yield {
                'action': 'relax',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': current,
                'highlighted_edges': [(current, neighbor)],
                'path': [],
                'description': f"A*: Checking ({current}, {neighbor}): g={tentative_g:.0f}, h={h:.0f}, f={tentative_g+h:.0f}",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': 0,
                    'steps': step,
                    'total_cost': 0
                },
                'step': step,
                'line': 2
            }

            # Update if better path found
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                h = _heuristic(neighbor, goal, nodes)
                f_score[neighbor] = tentative_g + h
                parent[neighbor] = current
                heapq.heappush(pq, (f_score[neighbor], neighbor))

    # No path found
    yield {
        'action': 'done',
        'nodes': nodes,
        'edges': edges,
        'start': start,
        'end': goal,
        'visited': list(visited),
        'current': None,
        'highlighted_edges': [],
        'path': [],
        'description': f"A*: No path found. Nodes visited: {len(visited)}",
        'stats': {
            'nodes_visited': len(visited),
            'path_length': 0,
            'steps': step,
            'total_cost': 0
        },
        'step': step,
        'line': 5
    }


def _heuristic(node, goal, nodes):
    """
    Heuristic function for A* - estimate distance to goal
    For layered graph, use layer distance as heuristic

    Args:
        node: Current node (layer_id, node_id)
        goal: Goal node (layer_id, node_id)
        nodes: List of all nodes

    Returns:
        Estimated cost from node to goal
    """
    # Extract layer information
    if isinstance(node, (tuple, list)) and isinstance(goal, (tuple, list)):
        current_layer = node[0]
        goal_layer = goal[0]

        # Layer distance * estimated cost per layer
        # Average edge weight is ~5, so use conservative estimate
        layer_distance = abs(goal_layer - current_layer)
        return layer_distance * 3  # Admissible (optimistic) estimate
    else:
        # Fallback for non-tuple nodes
        return 0


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': "A* Algorithm",
        'category': 'Graph Algorithms',
        'time_complexity': 'O((V + E) log V)',
        'space_complexity': 'O(V)',
        'description': 'Finds shortest weighted path using heuristic (f=g+h). More efficient than Dijkstra!',
        'code': '''def astar(graph, start, goal, heuristic):
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    pq = [(f_score[start], start)]
    visited = set()

    while pq:
        _, node = heapq.heappop(pq)
        if node in visited:
            continue
        if node == goal:
            return g_score[goal]
        visited.add(node)

        for neighbor, weight in graph[node]:
            tentative_g = g_score[node] + weight
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_score[neighbor], neighbor))

    return float('inf')'''
    }
