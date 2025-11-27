"""
Dijkstra's Shortest Path Algorithm
"""
import heapq


def dijkstra(arr, target=None):
    """
    Dijkstra's algorithm for finding shortest paths

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)

    Args:
        arr: Array to generate graph from
        target: Target node (optional)

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

    # Initialize distances
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0

    # Priority queue: (distance, node)
    pq = [(0, start_node)]
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
        'distances': distances.copy(),
        'description': f'Starting Dijkstra from node {start_node}',
        'line': 0
    }

    while pq:
        current_dist, current = heapq.heappop(pq)

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
            'distances': distances.copy(),
            'description': f'Processing node {current} with distance {current_dist}',
            'line': 1
        }

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
                'visited': list(visited),
                'current_node': current,
                'highlighted_edges': [(current, neighbor)],
                'path_edges': list(path_edges),
                'distances': distances.copy(),
                'description': f'Checking edge ({current}, {neighbor}): {distances[current]} + {weight} = {new_dist} vs {distances[neighbor]}',
                'line': 2
            }

            # Relax edge if shorter path found
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

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
                    'distances': distances.copy(),
                    'description': f'Updated distance to {neighbor}: {new_dist}',
                    'line': 3
                }

    # Done - show final shortest path tree
    yield {
        'action': 'done',
        'nodes': nodes,
        'edges': edges,
        'visited': list(visited),
        'current_node': None,
        'highlighted_edges': [],
        'path_edges': list(path_edges),
        'distances': distances,
        'description': f'Dijkstra complete. Shortest paths from {start_node}',
        'line': 5
    }


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
        'name': "Dijkstra's Algorithm",
        'category': 'Graph Algorithms',
        'time_complexity': 'O((V + E) log V)',
        'space_complexity': 'O(V)',
        'description': 'Finds shortest paths from a source node to all other nodes in a weighted graph.',
        'code': '''def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph[node]:
            new_dist = distances[node] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return distances'''
    }
