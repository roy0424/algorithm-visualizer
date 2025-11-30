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
    nodes, edges, adj_list, start, goal, node_scale = _generate_weighted_graph(arr)

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
        'node_scale': node_scale,
        'step': 0,
        'line': 0  # def dijkstra...
    }

    step = 0

    while pq:
        # Loop start
        yield {
            'action': 'loop',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': None,
            'highlighted_edges': [],
            'path': [],
            'description': "Dijkstra: Next iteration",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': 0
            },
            'node_scale': node_scale,
            'step': step,
            'line': 6  # while pq:
        }

        current_dist, current = heapq.heappop(pq)

        # Highlight pop
        yield {
            'action': 'pop',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"Dijkstra: Pop {current} with dist {current_dist:.1f}",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': int(current_dist)
            },
            'node_scale': node_scale,
            'step': step,
            'line': 7  # heapq.heappop(pq)
        }

        # Highlight visited check
        yield {
            'action': 'check_visit',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"Dijkstra: Checking if {current} already visited",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': int(current_dist)
            },
            'node_scale': node_scale,
            'step': step,
            'line': 8  # if node in visited
        }

        if current in visited:
            yield {
                'action': 'skip_visited',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': current,
                'highlighted_edges': [],
                'path': [],
                'description': f"Dijkstra: {current} already visited, skipping",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': 0,
                    'steps': step,
                    'total_cost': int(current_dist)
                },
                'node_scale': node_scale,
                'step': step,
                'line': 9  # continue
            }
            continue

        # Highlight goal check
        yield {
            'action': 'check_goal',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"Dijkstra: Is {current} the goal?",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': int(current_dist)
            },
            'node_scale': node_scale,
            'step': step,
            'line': 10  # if node == goal
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
                    'path_length': int(distances[goal]),
                    'steps': step,
                    'total_cost': int(distances[goal])
                },
                'node_scale': node_scale,
                'step': step,
                'line': 10  # if node == goal
            }
            return

        visited.add(current)
        step += 1

        # Show current node being processed (after marking visited)
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
            'node_scale': node_scale,
            'step': step,
            'line': 12  # visited.add(node)
        }

        # Check neighbors
        yield {
            'action': 'neighbors',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"Dijkstra: Exploring neighbors of {current}",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': 0
            },
            'node_scale': node_scale,
            'step': step,
            'line': 14  # for neighbor
        }
        for neighbor, weight in adj_list.get(current, []):
            if neighbor in visited:
                continue

            new_dist = distances[current] + weight

            # Highlight distance computation
            yield {
                'action': 'compute',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': current,
                'highlighted_edges': [(current, neighbor)],
                'path': [],
                'description': f"Dijkstra: Compute dist to {neighbor}: {distances[current]:.0f} + {weight} = {new_dist:.0f}",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': 0,
                    'steps': step,
                    'total_cost': 0
                },
                'node_scale': node_scale,
                'step': step,
                'line': 15  # new_dist calculation
            }

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
            'node_scale': node_scale,
            'step': step,
                'line': 14  # for neighbor, weight in graph[node]
            }

            # Relax edge if shorter path found
            yield {
                'action': 'check_better',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': current,
                'highlighted_edges': [(current, neighbor)],
                'path': [],
                'description': f"Dijkstra: Is {new_dist:.0f} < current dist to {neighbor}?",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': 0,
                    'steps': step,
                    'total_cost': 0
                },
                'node_scale': node_scale,
                'step': step,
                'line': 16  # if new_dist < distances[neighbor]
            }

            if new_dist < distances[neighbor]:
                yield {
                    'action': 'compare_update',
                    'nodes': nodes,
                    'edges': edges,
                    'start': start,
                    'end': goal,
                    'visited': list(visited),
                    'current': current,
                    'highlighted_edges': [(current, neighbor)],
                    'path': [],
                    'description': f"Dijkstra: Updating {neighbor} to {new_dist:.0f}",
                    'stats': {
                        'nodes_visited': len(visited),
                        'path_length': 0,
                        'steps': step,
                        'total_cost': 0
                    },
                    'node_scale': node_scale,
                    'step': step,
                    'line': 17  # distances[neighbor] = new_dist
                }

                distances[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

                yield {
                    'action': 'push_queue',
                    'nodes': nodes,
                    'edges': edges,
                    'start': start,
                    'end': goal,
                    'visited': list(visited),
                    'current': current,
                    'highlighted_edges': [(current, neighbor)],
                    'path': [],
                    'description': f"Dijkstra: Push {neighbor} with dist {new_dist:.0f} to queue",
                    'stats': {
                        'nodes_visited': len(visited),
                        'path_length': 0,
                        'steps': step,
                        'total_cost': 0
                    },
                    'node_scale': node_scale,
                    'step': step,
                    'line': 18  # heapq.heappush
                }

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
        'node_scale': node_scale,
        'step': step,
        'line': 20  # return float('inf')
    }


def _generate_weighted_graph(arr):
    """
    Generate a layered weighted graph (neural network style)
    Structure: Start (left) -> Hidden Layers -> Goal (right)

    Args:
        arr: Input array (first element determines number of layers 3-10)

    Returns:
        Tuple of (nodes, edges, adjacency_list, start_node, goal_node, node_scale)
    """
    level = arr[0] if arr and arr[0] > 0 else 4

    # Deterministic seed per level so each level shows a fixed graph
    random.seed(level)

    # Determine number of layers (3-10)
    num_layers = max(3, min(int(level), 10))

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

    # Connect layers: ensure full fan-out from start and full fan-in to goal
    for layer_idx in range(len(layers) - 1):
        current_layer = layers[layer_idx]
        next_layer = layers[layer_idx + 1]

        targets_per_node = {}
        if layer_idx == 0:
            # Start -> all nodes in next layer
            targets_per_node = {node: next_layer for node in current_layer}
        elif layer_idx == len(layers) - 2:
            # All nodes in previous layer -> goal
            targets_per_node = {node: next_layer for node in current_layer}
        else:
            # For deeper graphs, reduce connections to limit overlap
            dense = len(layers) < 7
            min_conn = 2 if dense else 1
            max_conn = 3 if dense else 2
            for node in current_layer:
                upper = min(max_conn, len(next_layer))
                lower = min(min_conn, upper)
                num_connections = random.randint(lower, upper) if upper > 0 else 0
                targets_per_node[node] = random.sample(next_layer, num_connections)

        for node, targets in targets_per_node.items():
            for target in targets:
                # Avoid duplicate edges
                if any(e[0] == node and e[1] == target for e in edges):
                    continue

                weight = random.randint(1, 10)

                # Add edge (directed: current -> next)
                edges.append((node, target, weight))
                adj_list[node].append((target, weight))
                # For pathfinding, make it bidirectional
                adj_list[target].append((node, weight))

    # Scale nodes slightly down as layers increase to avoid overlap
    node_scale = max(0.6, 1.05 - num_layers * 0.05)

    return nodes, edges, adj_list, start, goal, node_scale


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
