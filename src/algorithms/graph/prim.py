"""
Prim's Minimum Spanning Tree Algorithm
"""
import heapq


def prim(arr, target=None):
    """
    Prim's algorithm for finding Minimum Spanning Tree

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)

    Args:
        arr: Array to generate graph from
        target: Not used (for consistency)

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

    # MST edges
    mst_edges = set()
    visited = set([start_node])

    # Priority queue: (weight, from_node, to_node)
    pq = []
    for neighbor, weight in adj_list.get(start_node, []):
        heapq.heappush(pq, (weight, start_node, neighbor))

    total_weight = 0

    # Initial state
    yield {
        'action': 'start',
        'nodes': nodes,
        'edges': edges,
        'visited': list(visited),
        'current_node': start_node,
        'highlighted_edges': [],
        'path_edges': [],
        'description': f'Starting Prim from node {start_node}',
        'line': 0
    }

    while pq and len(visited) < len(nodes):
        weight, from_node, to_node = heapq.heappop(pq)

        # Skip if already visited
        if to_node in visited:
            continue

        # Add edge to MST
        mst_edges.add((from_node, to_node))
        visited.add(to_node)
        total_weight += weight

        # Show edge being added
        yield {
            'action': 'add_edge',
            'nodes': nodes,
            'edges': edges,
            'visited': list(visited),
            'current_node': to_node,
            'highlighted_edges': [(from_node, to_node)],
            'path_edges': list(mst_edges),
            'description': f'Adding edge ({from_node}, {to_node}) with weight {weight} to MST',
            'line': 1
        }

        # Add new edges to priority queue
        for neighbor, edge_weight in adj_list.get(to_node, []):
            if neighbor not in visited:
                # Show edge being considered
                yield {
                    'action': 'consider',
                    'nodes': nodes,
                    'edges': edges,
                    'visited': list(visited),
                    'current_node': to_node,
                    'highlighted_edges': [(to_node, neighbor)],
                    'path_edges': list(mst_edges),
                    'description': f'Considering edge ({to_node}, {neighbor}) with weight {edge_weight}',
                    'line': 2
                }

                heapq.heappush(pq, (edge_weight, to_node, neighbor))

    # Done
    yield {
        'action': 'done',
        'nodes': nodes,
        'edges': edges,
        'visited': list(visited),
        'current_node': None,
        'highlighted_edges': [],
        'path_edges': list(mst_edges),
        'description': f'Prim complete. MST weight: {total_weight}, Edges: {len(mst_edges)}',
        'line': 4
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
        'name': "Prim's Algorithm",
        'category': 'Graph Algorithms',
        'time_complexity': 'O((V + E) log V)',
        'space_complexity': 'O(V)',
        'description': 'Finds the Minimum Spanning Tree (MST) by greedily selecting minimum weight edges.',
        'code': '''def prim(graph, start):
    mst = set()
    visited = set([start])
    edges = [(weight, start, to) for to, weight in graph[start]]
    heapq.heapify(edges)

    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst.add((frm, to, weight))

            for next_to, next_weight in graph[to]:
                if next_to not in visited:
                    heapq.heappush(edges, (next_weight, to, next_to))

    return mst'''
    }
