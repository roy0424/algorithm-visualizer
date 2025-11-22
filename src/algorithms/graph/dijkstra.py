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
    Generate a weighted graph from an array

    Args:
        arr: Input array

    Returns:
        Tuple of (nodes, edges, adjacency_list)
    """
    # Get unique nodes (limit to 8 for visualization)
    nodes = sorted(list(set(arr)))[:8]

    if len(nodes) < 2:
        return nodes, [], {}

    # Generate edges with weights
    edges = []
    adj_list = {node: [] for node in nodes}

    # Connect based on original array order
    for i in range(len(arr) - 1):
        if arr[i] in nodes and arr[i+1] in nodes:
            u, v = arr[i], arr[i+1]
            weight = abs(u - v) % 10 + 1  # Weight between 1-10

            # Add edge (undirected)
            edge_exists = False
            for existing_edge in edges:
                if (existing_edge[0] == u and existing_edge[1] == v) or \
                   (existing_edge[0] == v and existing_edge[1] == u):
                    edge_exists = True
                    break

            if not edge_exists:
                edges.append((u, v, weight))
                adj_list[u].append((v, weight))
                adj_list[v].append((u, weight))

    # Ensure graph is connected
    if len(edges) < len(nodes) - 1:
        for i in range(len(nodes) - 1):
            u, v = nodes[i], nodes[i+1]
            weight = abs(u - v) % 10 + 1

            # Check if edge already exists
            if not any((n, w) for n, w in adj_list[u] if n == v):
                edges.append((u, v, weight))
                adj_list[u].append((v, weight))
                adj_list[v].append((u, weight))

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
