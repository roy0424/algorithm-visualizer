"""
Dijkstra's Shortest Path Algorithm on Weighted Graph
"""
import heapq
import random


def dijkstra_weighted(arr, target=None):
    """
    Dijkstra's algorithm for finding shortest path in a weighted graph

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

    # Generate weighted graph
    nodes, edges, adj_list, start, goal = _generate_weighted_graph(arr)

    if not nodes:
        return

    # Initialize distances
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0

    # Priority queue: (distance, node)
    pq = [(0, start)]
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
        'description': f"Dijkstra: Starting from node {start} to {goal}",
        'stats': {'nodes_visited': 0, 'path_length': 0, 'steps': 0, 'total_cost': 0},
        'step': 0,
        'line': 0
    }

    step = 0

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        step += 1

        # Show current node being processed
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
            'description': f"Dijkstra: Visiting node {current} (distance: {current_dist:.1f})",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': int(current_dist)
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
                'description': f"Dijkstra: Goal reached! Cost: {int(distances[goal])}, Nodes visited: {len(visited)}",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': len(path),
                    'steps': step,
                    'total_cost': int(distances[goal])
                },
                'step': step,
                'line': 5
            }
            return

        # Check neighbors
        for neighbor, weight in adj_list.get(current, []):
            if neighbor in visited:
                continue

            new_dist = distances[current] + weight

            # Highlight edge being considered
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
                'description': f"Dijkstra: Checking edge ({current}, {neighbor}): {distances[current]:.0f} + {weight} = {new_dist:.0f}",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': 0,
                    'steps': step,
                    'total_cost': 0
                },
                'step': step,
                'line': 2
            }

            # Relax edge if shorter path found
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

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
        'description': f"Dijkstra: No path found. Nodes visited: {len(visited)}",
        'stats': {
            'nodes_visited': len(visited),
            'path_length': 0,
            'steps': step,
            'total_cost': 0
        },
        'step': step,
        'line': 5
    }


def _generate_weighted_graph(arr):
    """
    Generate a layered weighted graph (neural network style)
    Structure: Start (left) → Hidden Layers → Goal (right)

    Args:
        arr: Input array (first element determines number of layers)

    Returns:
        Tuple of (nodes, edges, adjacency_list, start_node, goal_node)
    """
    # Set fixed seed for consistency
    random.seed(42)

    # Determine number of layers (3-5)
    size = arr[0] if arr and arr[0] > 0 else 15
    num_layers = min(max(3, size // 10), 5)

    # Build layered structure
    nodes = []
    edges = []
    adj_list = {}

    # Layer 0: Start node
    start = (0, 0)
    nodes.append(start)
    adj_list[start] = []

    # Middle layers: 3-5 nodes per layer
    layers = [[start]]
    for layer_id in range(1, num_layers - 1):
        layer_nodes = []
        num_nodes_in_layer = random.randint(3, 5)

        for node_idx in range(num_nodes_in_layer):
            node = (layer_id, node_idx)
            nodes.append(node)
            adj_list[node] = []
            layer_nodes.append(node)

        layers.append(layer_nodes)

    # Last layer: Goal node
    goal = (num_layers - 1, 0)
    nodes.append(goal)
    adj_list[goal] = []
    layers.append([goal])

    # Connect layers: each node connects to 2-3 nodes in next layer
    for layer_idx in range(len(layers) - 1):
        current_layer = layers[layer_idx]
        next_layer = layers[layer_idx + 1]

        for node in current_layer:
            # Connect to 2-3 random nodes in next layer (reduced from 2-4)
            num_connections = min(random.randint(2, 3), len(next_layer))
            targets = random.sample(next_layer, num_connections)

            for target in targets:
                # Generate weight
                weight = random.randint(1, 10)

                # Add edge (directed: current -> next)
                edges.append((node, target, weight))
                adj_list[node].append((target, weight))
                # For pathfinding, make it bidirectional
                adj_list[target].append((node, weight))

    # Add one skip connection for alternative path (reduced from 1-2)
    if len(layers) >= 3:
        layer_idx = 0  # Only from first layer
        current_layer = layers[layer_idx]
        skip_layer = layers[layer_idx + 2]

        # Add just 1 skip connection
        node = random.choice(current_layer)
        target = random.choice(skip_layer)

        # Check if edge already exists
        exists = any((e[0] == node and e[1] == target) for e in edges)

        if not exists:
            weight = random.randint(5, 12)
            edges.append((node, target, weight))
            adj_list[node].append((target, weight))
            adj_list[target].append((node, weight))

    return nodes, edges, adj_list, start, goal


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': "Dijkstra's Algorithm",
        'category': 'Graph Algorithms',
        'time_complexity': 'O((V + E) log V)',
        'space_complexity': 'O(V)',
        'description': 'Finds shortest weighted path. Explores all directions uniformly.',
        'code': '''def dijkstra(graph, start, goal):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, node = heapq.heappop(pq)
        if node in visited:
            continue
        if node == goal:
            return distances[goal]
        visited.add(node)

        for neighbor, weight in graph[node]:
            new_dist = distances[node] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return float('inf')'''
    }
