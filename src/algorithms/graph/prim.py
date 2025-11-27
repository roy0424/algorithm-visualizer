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
